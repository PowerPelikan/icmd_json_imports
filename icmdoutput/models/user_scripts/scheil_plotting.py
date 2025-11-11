'''Module for plotting Solidification data'''
import pandas as pd
import plotly.express as px
from icmdoutput.models.solidification import Solidification

class Scheil(Solidification):
    '''Methods to Plot Solidification Data, not useable for parameter'''
    def __init__(self, path: str, modelname: str):
        super().__init__(path, modelname)

        self.temp_by_phase = self._compute_temp_by_phase()


    def _get_present_phases(self, row, threshold):
        df = self.get_phase_fraction()
        phase_columns = [
            col for col in df.columns
            if col != 'Temperature in C' and col != 'SOLID'
        ]
        return [ph for ph in phase_columns if row[ph] > threshold]

    def _compute_temp_by_phase(self, threshold = 1e-6):
        ''' Returns a better/other Phase Region DataFrame, if the ICMD output doenst seems right '''
        phase_df = self.get_phase_fraction(parameter=False)
        temp_df = self.get_temperatures()

        present = phase_df.apply(
            lambda r: self._get_present_phases(r, threshold),
            axis=1
        )
        mapped = pd.DataFrame({
            'Temperature in C': temp_df['Temperatere in C'].values,
            'Phase Region': present.apply(lambda ph: '+'.join(sorted(ph)))
        })
        return mapped

    def get_temp_by_phase(self):
        '''return temperature by phases'''
        return self.temp_by_phase

    def get_scheil_df(self, threshold=1e-6):
        '''Return Dataframe for Scheil plot, calulated from compute_temp_by_phase'''
        base = self.get_percent_solidified_molar()
        phase_info = self._compute_temp_by_phase(threshold)
        return pd.concat([base, phase_info], axis=1).iloc[:-1]

    def scheil_plot(self, temp_unit = 'C', plotname='', user_script=False, threshold= 1e-6):
        '''Returns a Plotly fig with a Scheil Plot'''
        df = self.get_scheil_df(threshold) if user_script else self.get_data_for_scheil_plot(temp_unit)

        fig = px.line(
            df,
            x='Percent solidified molar',
            y=f'Temperature in {temp_unit}',
            color='Phase Region',
            title=plotname
            )
        fig.update_traces(line={'width': 3})
        fig.update_layout(font={'size': 16}, title_font={'size': 22})
        return fig

    def _scheil_plot_fig(self, df, temp_col, plotname, log, y_range):
        fig = px.line(
            df,
            x=temp_col,
            y='Phase Fraction',
            color='Phase',
            log_y=log,
            title=plotname
        )

        fig.update_traces(line={'width':2})
        if y_range:
            fig.update_yaxes(range=y_range)
        elif log:
            fig.update_yaxes(range=[-4,0])
        fig.update_layout(
            font={"size": 16},
            title_font={"size": 22},
            xaxis_title=temp_col,
            yaxis_title= 'Phase fraction in mole'
        )
        return fig

    def scheil_step_plt(self, parameter=False, temp_unit='C', plotname='', log=True, y_range=None):
        '''Plot phase fraction over Temperature'''
        df = self.get_phase_fraction(parameter=parameter, temp_unit=temp_unit)
        temp_col = f'Temperature in {temp_unit}'

        phase_cols = [p for p in self.get_phase_names() if p != 'SOLID' and p in df.columns]
        df_long = df.melt(
            id_vars = [temp_col],
            value_vars = phase_cols,
            var_name = 'Phase',
            value_name='Phase Fraction'
        ).sort_values(temp_col)

        return self._scheil_plot_fig(df_long, temp_col, plotname, log, y_range)
