"""
This file contains the definition of data objects used across the application.
"""
import dataclasses
import enum
from typing import List, Dict
import plotly.graph_objects as go
import pytz
import pandas as pd
import numpy as np
from txp.common.utils.plotter_utils import FFTPlotter


# Accessible Constants values
# Provide some constant values that can be used across the APP code
# To determine which type of plotly object is being processed
SIGNAL_TRACE_TYPE_KEY='signal-type'
SIGNAL_TRACE_TYPE_VALUE='signal-trace'  # Describes the trace as a Signal Trace in the plot
FAILURE_FREQUENCY_TRACE_VALUE='failure-frequency-trace'  # Describes the trace as a Failure Frequency trace


class SampleDistribution(enum.Enum):
    """Class to encapsulate the data distribution to be downloaded from the
    databases for visualizations"""

    LAST_7_DAYS = 0
    CURRENT_DAY = 1


def add_vertical_3d_failure_freq(figure, freq_y):
    """Adds a vertical surface in the XYZ plane, in order to show a
    visual guide for the failure frequencies.

    Args
        figure: a json plotly figure to add the freq_y vertical surface.
        freq_y: the value of Y in the plotly figure. This is the frequency
            axis.
    """
    x_values = []
    max_z_val = 0

    # Gets all the X-values (datetime axis) active in the plot.
    # Gets the max_z_val found
    for scatter_data in figure["data"]:
        if scatter_data['customdata'][0] == SIGNAL_TRACE_TYPE_VALUE:
            x_values.append(scatter_data["x"][0])
            max_z_val = max(max_z_val, np.max(scatter_data["z"]))

    # Create the vertical plane
    zz = np.linspace(0, max_z_val, 100)
    XX, ZZ = np.meshgrid(x_values, zz)
    YY = freq_y * np.ones(XX.shape)

    # Adds the surface to the plot. The `customdata` attribute value
    #   allows to identify this trace as a non-signal trace.
    fault_surface = go.Surface(
        x=XX,
        y=YY,
        z=ZZ,
        showscale=False,
        opacity=0.2,
        customdata=(FAILURE_FREQUENCY_TRACE_VALUE,)
    )
    figure["data"].append(fault_surface.to_plotly_json())

    return figure


@dataclasses.dataclass
class VibrationCascadeGraph:
    """This object represents the Cascade graph of a list of 3D vibration curves

    Args:
        sample_distribution: The sample distribution used to build this graph.
        raw_signals: The list of raw signals pulled from the tabular database.
        machine_id: The ID of the machine to which the signals belong to.
        num_axis: The num of axis measured by the sensor.
    """

    sample_distribution: SampleDistribution
    raw_signals: List[Dict]
    machine_id: str
    tenant_id: str
    num_axis: int = 3
    sampling_frequency: int = 3611

    def __post_init__(self):
        self._x_axis_name = "Time"
        self._y_axis_name = "Frequency (Hz)"
        self._z_axis_name = "Amplitude (A)"
        self._mean_trace_name = "Arithmetic mean"
        self.fft_traces: List[List[go.Scatter3d]] = list(
            map(self.transform_signal_to_trace, self.raw_signals)
        )
        self.mean_trace: List[go.Scatter3d] = self.compute_axis_mean(self.fft_traces)

    def get_fig(self) -> List[go.Figure]:
        """Returns the list of Figures per axes"""
        figs = []
        x_values = []
        max_z_val = 0
        for i in range(self.num_axis):
            traces = [self.mean_trace[i]]
            for fft_trace in self.fft_traces:
                traces.append(fft_trace[i])
                x_values.append(fft_trace[i].x[0])
                max_z_val = max(max_z_val, np.max(fft_trace[i].z))

            traces.reverse()

            fig = go.Figure(
                data=traces,
                layout=go.Layout(
                    scene=dict(
                        xaxis=dict(title=self._x_axis_name),
                        yaxis=dict(title=self._y_axis_name),
                        zaxis=dict(title=self._z_axis_name),
                    )
                )
            )

            figs.append(fig)
        return figs

    @classmethod
    def change_utc_timezone(cls, timestamp):
        utc = pytz.timezone("UTC")
        timezone = pytz.timezone("America/Mexico_City")
        date_time = pd.to_datetime(timestamp)
        localized_timestamp = utc.localize(date_time)
        new_timezone = localized_timestamp.astimezone(timezone)
        return new_timezone

    def compute_axis_mean(
        self, signals: List[List[go.Scatter3d]]
    ) -> List[go.Scatter3d]:
        """Compute the mean of the frequencies of the signals for each axis.

        The returns the list of the resulting traces for each axis.
        """
        # TODO: Beware, this is a long one-liner, you can get hurt! Please refactor
        signals_numpy = np.mean(
            np.array([[np.array(s.z) for s in signal] for signal in signals]),
            axis=0,
            dtype=np.float64,
        )
        axis_plots = []
        for dimension_axis in range(0, len(signals_numpy)):
            plt = FFTPlotter(
                signals_numpy[dimension_axis],
                signals[0][dimension_axis].y,  # The frequency axis
                self.sampling_frequency,
                compute_signal_frequency_amplitude_axis=False,
            )
            axis_plots.append(plt)

        traces_3d = []
        for i, axis_plt in enumerate(axis_plots):
            trace = go.Scatter3d(
                x=[self._mean_trace_name] * axis_plt.signal_amplitude_axis.__len__(),
                y=axis_plt.signal_frequency_amplitude_axis,
                z=axis_plt.signal_amplitude_axis,
                mode="lines",
                visible=True,
                name=f"Promedio",
                customdata=(SIGNAL_TRACE_TYPE_VALUE,)
            )
            traces_3d.append(trace)

        return traces_3d

    def transform_signal_to_trace(self, signal: Dict) -> List[go.Scatter3d]:
        """Transforms a signal taken from the TXP time series collection.

        Returns the Scatter3D object instance for that signal.
        The __len__() vaue of the return List is equal to the num_axis from the signal.

        Args:
            signal: A list of Dict representations of a signal. The dictionary
                keys are the column names on the table.
        """
        axis_plots = []
        for dimension_axis in range(0, len(signal["data"])):
            plt = FFTPlotter(
                signal["data"][dimension_axis]["values"], None, self.sampling_frequency
            )
            axis_plots.append(plt)

        traces_3d = []
        for idx, axis_plt in enumerate(axis_plots):
            trace = go.Scatter3d(
                x=[
                    self.change_utc_timezone(signal["observation_timestamp"]).strftime(
                        "%Y-%M-%D \n %H:%M:%S"
                    )
                ]
                * axis_plt.frequency_axis.__len__(),
                y=axis_plt.frequency_axis,
                z=axis_plt.sample_count
                * np.abs(axis_plt.signal_frequency_amplitude_axis),
                mode="lines",
                visible=True,
                name=f"{signal['rpm'][idx]:.2f} RPM",
                customdata=(SIGNAL_TRACE_TYPE_VALUE,)
            )
            traces_3d.append(trace)

        return traces_3d


@dataclasses.dataclass
class FrequencyAmplitudeVariationGraph:
    """Represents the 2D Graph to view the variation of amplitude for the
    given instance."""

    x_values: List  # should be the dates
    y_values: List  # should be the Amplitude values
    freq: float  # the frequency value selected by the user

    def get_fig(self) -> go.Figure:
        line = go.Scatter(x=self.x_values, y=self.y_values, showlegend=False)
        fig = go.Figure()
        fig.add_trace(line)
        fig.update_layout(
            title=f"Frequency Variation over time for {self.freq:.2f} Hz.",
            xaxis_title="Tiempo",
            yaxis_title="Amplitude",
        )
        return fig


@dataclasses.dataclass
class AreaVariationGraph:
    """Represents the 2D line of the variation of the area for a given
    list of lines"""

    x_values: List  # should be the dates
    y_values: List  # should be the Amplitude values

    def get_fig(self) -> go.Figure:
        line = go.Scatter(x=self.x_values, y=self.y_values, showlegend=False)
        fig = go.Figure()
        fig.add_trace(line)
        fig.update_layout(
            title=f"Area variation over time for selected samples",
            xaxis_title="Tiempo",
            yaxis_title="Area under the line",
        )
        return fig
