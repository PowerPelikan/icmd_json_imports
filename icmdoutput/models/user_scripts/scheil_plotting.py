import pandas as pd
import plotly.express as px
from icmdoutput.models.solidification import Solidification

class Scheil(Solidification):

    def __init__(self, path: str, modelname: str):
        super().__init__(path, modelname)

        self.temp_by_phase = self.__new_temp_by_phase()


    def __get_present_phases(self, row, threshhold):
        df = self.get_phase_fraction()
        phase_columns = [col for col in df.columns if col != 'Temperature in C' and col != 'SOLID']
        return [phase for phase in phase_columns if row[phase]>threshhold]

    def __new_temp_by_phase(self, threshhold = 1e-6):
        ''' Returns a better/other Phase Region DataFrame, if the ICMD outptut is wierd '''

        phase_region = self.get_phase_fraction(parameter=False).apply(lambda row: self.__get_present_phases(row, threshhold), axis=1)
        df_present = pd.DataFrame(
            list(zip( self.get_temperatures()['Temperature in C'].values, phase_region.apply(lambda phase: '+'.join(sorted(phase))).values)),
            columns=['Temperature in C', 'Phase Region']
        )

        return df_present

    def get_temp_by_phase(self):

        return self.temp_by_phase
    
    def get_scheil_df(self, threshhold=1e-6):

        return pd.concat([self.get_percent_solidified_molar(), self.__new_temp_by_phase(threshhold)], axis=1).iloc[:-1]

    def scheil_plot(self, tempunit = 'C', plotname='', userscript=False, threshhold= 1e-6):
        '''Returns a Plotly fig with a Scheil Plot'''

        if userscript:
            df = self.get_scheil_df(threshhold)
        else:
            df = self.get_data_for_scheil_plot(tempunit)

        fig = px.line(df, x='Percent solidified molar', y='Temperature in '+tempunit, color='Phase Region', title=plotname)
        fig.update_traces(line={'width':5})
        fig.update_layout(
            font=dict(
                size=18
            ),
            title_font=dict(
                size=24
            )
        )

        return fig 

    def __scheil_plot_fig_dif(self, df, temps, plotname, log, minmax):
        fig = px.line(df,
                      x=temps,
                      y='Phase Fraction',
                      color='Phase',
                      log_y=log, title=plotname)

        fig.update_traces(line={'width':3})
        if minmax is not None:
            fig.update_yaxes(range=minmax)
        if log:
            if minmax is None:
                fig.update_yaxes(range=[-4,0])

        fig.update_layout(
            font={"size": 18},
            title_font={"size": 24},
            xaxis_title=temps,
            yaxis_title= 'Phase fraction in mol'
        )
        return fig

    def scheil_step_plt(self, parameter=False, tempunit='C', plotname='', log=True, minmax=None):
        '''Plot phase fraction over Temperature'''

        df = self.get_phase_fraction(parameter=parameter, temp_unit=tempunit)
        temp_col = 'Temperature in ' + tempunit
        phase_cols = self.get_phase_names()
        phase_cols.remove('SOLID')

        phase_cols = [col for col in df.columns if col in phase_cols + [temp_col] ]

        if parameter:
            df_grouped = df.groupby(self.get_components)
            fig_list = []
            for comp, group in df_grouped:
                df_long = group.melt(
                    id_vars = [temp_col],
                    value_vars=phase_cols,
                    var_name='Phase',
                    value_name='Phase Fraction'
                )



        df_long = df.melt(
            id_vars = [temp_col],
            value_vars=phase_cols,
            var_name='Phase',
            value_name='Phase Fraction'
        )

        df_long = df_long.sort_values(temp_col)

        fig = self.__scheil_plot_fig_dif(df_long, temp_col, plotname=plotname, log=log, minmax=minmax)


        return fig
