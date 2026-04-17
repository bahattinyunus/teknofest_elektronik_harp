import time
import os
import sys
import numpy as np
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import box

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.signal_processing.analyzer import SpectrumAnalyzer, ParameterExtractor
from src.ai_engine.classifier import SignalClassifier
from src.ai_engine.autonomy_manager import AutonomyManager
from src.signal_processing.lpi_detector import LPIDetector
from src.jamming_logic.jammers import JammerCoordinator
from src.simulation.scenario_manager import ScenarioManager

console = Console()

class AegisDashboard:
    def __init__(self):
        self.sample_rate = 1e6
        self.duration = 0.01
        self.scen = ScenarioManager(self.sample_rate)
        self.sa = SpectrumAnalyzer(self.sample_rate)
        self.pe = ParameterExtractor(self.sample_rate)
        self.clf = SignalClassifier()
        self.lpi = LPIDetector(self.sample_rate)
        self.coord = JammerCoordinator(self.sample_rate)
        self.autonomy = AutonomyManager(self.clf, self.lpi, self.coord)
        
        self.scenarios = [
            "Clear Sky",
            "Long Range Search",
            "Tracking Radar",
            "LPI Stealth Radar",
            "Swarm Incursion",
            "Fire Control Radar",
            "Analog Telsiz"
        ]
        self.current_idx = 0
        self.is_running = True

    def make_header(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            Text("🛰️ AEGIS-AI OMEGA v3.0 | COGNITIVE ELECTRONIC WARFARE SYSTEM", style="bold cyan"),
            Text(time.ctime(), style="dim white"),
        )
        return Panel(grid, style="white on blue", box=box.DOUBLE)

    def make_spectrum_panel(self, freqs, mags) -> Panel:
        # Mini ASCII Plot for spectrum
        max_height = 10
        width = 60
        plot = []
        
        # Resample mags to width
        indices = np.linspace(0, len(mags)-1, width).astype(int)
        resp_mags = mags[indices]
        resp_mags = (resp_mags / (np.max(resp_mags) + 1e-9) * max_height).astype(int)
        
        for h in range(max_height, 0, -1):
            line = ""
            for m in resp_mags:
                if m >= h:
                    line += "█"
                elif m >= h - 0.5:
                    line += "▄"
                else:
                    line += " "
            plot.append(line)
            
        plot_txt = "\n".join(plot)
        return Panel(plot_txt, title="[bold green]Real-time Spectrum (PSD)[/bold green]", border_style="green", box=box.ROUNDED)

    def make_threat_table(self) -> Panel:
        table = Table(box=box.SIMPLE, expand=True)
        table.add_column("Threat", style="cyan")
        table.add_column("Risk", justify="center")
        table.add_column("Confidence", justify="center")
        table.add_column("Strategy", style="magenta")

        recent = self.autonomy.threat_log[-8:]
        for t in reversed(recent):
            risk_color = "red" if t['risk'] >= 8 else ("yellow" if t['risk'] >= 5 else "green")
            table.add_row(
                t['threat'],
                Text(str(t['risk']), style=risk_color),
                f"{t['confidence']:.0%}",
                t['strategy']
            )
        return Panel(table, title="[bold red]Active Threat Log[/bold red]", border_style="red")

    def make_system_status(self) -> Panel:
        assessment = self.autonomy.risk_assessment()
        status = Table.grid(expand=True)
        status.add_row("System Mode:", " [bold green]AUTONOMOUS[/bold green]")
        status.add_row("Risk Level:", f" [bold]{assessment['threat_level']}[/bold]")
        status.add_row("Weighted Risk:", f" {assessment['risk_score']}/10")
        
        # Jammer status
        jam_active = "YES" if self.coord.active_assignments else "NO"
        jam_style = "bold red" if jam_active == "YES" else "dim"
        status.add_row("ET Active:", f" [{jam_style}]{jam_active}[/{jam_style}]")
        
        if self.coord.swarm_mode:
            status.add_row("Swarm Suppression:", " [bold magenta]ENGAGED[/bold magenta]")

        return Panel(status, title="[bold yellow]Unit Status[/bold yellow]", border_style="yellow")

    def run(self):
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        layout["main"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1)
        )
        layout["left"].split_column(
            Layout(name="spectrum"),
            Layout(name="threats")
        )

        with Live(layout, refresh_per_second=2, screen=True):
            while self.is_running:
                scenario_name = self.scenarios[self.current_idx % len(self.scenarios)]
                _, signal = self.scen.get_scenario_signal(scenario_name, self.duration)
                
                # Signal Processing
                params = self.pe.estimate_parameters(signal)
                freqs, mags = self.sa.compute_fft(signal)
                
                # Autonomy
                self.autonomy.process_detection(freqs, mags, raw_signal=signal, params=params)
                
                # Update UI
                layout["header"].update(self.make_header())
                layout["spectrum"].update(self.make_spectrum_panel(freqs, mags))
                layout["threats"].update(self.make_threat_table())
                layout["right"].update(self.make_system_status())
                layout["footer"].update(Panel(f"CURRENT SCENARIO: [bold yellow]{scenario_name}[/bold yellow] | Press Ctrl+C to exit", box=box.MINIMAL))
                
                time.sleep(1.2)
                self.current_idx += 1

if __name__ == "__main__":
    dash = AegisDashboard()
    try:
        dash.run()
    except KeyboardInterrupt:
        pass
