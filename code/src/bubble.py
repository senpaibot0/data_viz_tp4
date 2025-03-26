'''
    This file contains the code for the bubble plot.
'''

import plotly.express as px
import hover_template

def get_plot(my_df, gdp_range, co2_range):
    '''
        Generates the bubble plot.

        The x and y axes are log scaled, and there is
        an animation between the data for years 2000 and 2015.

        The discrete color scale (sequence) to use is Set1 (see : https://plotly.com/python/discrete-color/)

        The markers' maximum size is 30 and their minimum size is 6.

        Args:
            my_df: The dataframe to display
            gdp_range: The range for the x axis
            co2_range: The range for the y axis
        Returns:
            The generated figure
    '''
    # Create the animated bubble chart using Plotly Express
    fig = px.scatter(
        my_df,
        x="GDP",
        y="CO2",
        size="Population",
        color="Continent",
        animation_frame="Year",  # Animate based on the 'Year' column
        hover_name="Country Name",
        log_x=True,  # Log scale for x-axis (GDP)
        log_y=True,  # Log scale for y-axis (CO2)
        range_x=gdp_range,  # Set x-axis range
        range_y=co2_range,  # Set y-axis range
        size_max=30,  # Maximum marker size
        color_discrete_sequence=px.colors.qualitative.Set1  # Use Set1 color sequence
    )
    
    # Ensure minimum marker size is 6 by adjusting the figure's data
    for frame in fig.frames:
        for trace in frame.data:
            if 'marker' in trace and 'size' in trace['marker']:
                trace['marker']['sizemin'] = 6

    return fig

def update_animation_hover_template(fig):
    '''
        Sets the hover template of the figure,
        as well as the hover template of each
        trace of each animation frame of the figure

        Args:
            fig: The figure to update
        Returns:
            The updated figure
    '''
    # Get the hover template from hover_template.py
    hover_temp = hover_template.get_bubble_hover_template()
    
    # Update the main figure's hover template
    fig.update_traces(hovertemplate=hover_temp)
    
    # Update the hover template for each frame in the animation
    for frame in fig.frames:
        for trace in frame.data:
            trace.hovertemplate = hover_temp
    
    return fig

def update_animation_menu(fig):
    '''
        Updates the animation menu to show the current year, and to remove
        the unnecessary 'Stop' button.

        Args:
            fig: The figure containing the menu to update
        Returns:
            The updated figure
    '''
    # Update the animation menu buttons
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        args=[None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                        label="Play",
                        method="animate"
                    ),
                    # Remove the 'Stop' button by not including a pause option
                ],
                direction="left",
                pad={"r": 10, "t": 87},
                showactive=False,
                type="buttons",
                x=0.1,
                xanchor="right",
                y=0,
                yanchor="top"
            )
        ],
        # Add a slider with year labels
        sliders=[dict(
            steps=[
                dict(args=[[f.name], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                     label=str(f.name), method="animate") for f in fig.frames
            ],
            active=0,
            currentvalue={"prefix": "Year: ", "font": {"size": 20}},
            pad={"t": 50}
        )]
    )
    return fig

def update_axes_labels(fig):
    '''
        Updates the axes labels with their corresponding titles.

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    fig.update_layout(
        xaxis_title="GDP per capita ($ USD)",
        yaxis_title="CO2 emissions per capita (metric tonnes)"
    )
    return fig

def update_template(fig):
    '''
        Updates the layout of the figure, setting
        its template to 'simple_white'

        Args:
            fig: The figure to update
        Returns:
            The updated figure
    '''
    fig.update_layout(template="simple_white")
    return fig

def update_legend(fig):
    '''
        Updates the legend title

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    fig.update_layout(legend_title_text="Continent")
    return fig