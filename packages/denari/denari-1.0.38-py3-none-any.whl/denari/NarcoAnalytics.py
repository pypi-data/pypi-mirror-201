import pandas as pd
import plotly.graph_objects as go
import datetime as dt
from .TaxTools import TaxTools as tax

class NarcoAnalytics():
    #APPEARANCE
    def color_list(category_list, colors='basic') -> list:
        """
        Generates a list of colors for the provided category list based on the specified color set.
        
        :param category_list: List of categories for which colors are needed
        :param colors: Name of the color set to use ('basic', 'one', 'profit', or 'binary-p/b'); default is 'basic'
        :return: List of colors corresponding to the category_list, based on the specified color set
        """
        color_sets = {
            'basic': ['#FFA89E', '#A4DEF5', '#ACE1AD'],
            'one': ['#60FA5A', '#FF8791', '#75AEFA', '#FA69B9', '#9B70A4', '#FAF682', '#FACC75'],
            'profit': ['#60FA5A', '#FF8791', '#75AEFA'],
            'binary-p/b': ['#75AEFA', '#FA69B9']
        }

        num_categories = len(category_list)
        default_color = 'lightslategray'
        color_list = [default_color] * num_categories

        selected_color_set = color_sets[colors]
        trimmed_color_set = selected_color_set[:num_categories]

        for color in trimmed_color_set:
            color_list[trimmed_color_set.index(color)] = color

        return color_list

    #GENERAL
    def column_set(df: pd.DataFrame, group: str, group_by: str, ascending=True) -> list:
        """
        Sorts the DataFrame by the specified 'group_by' column and returns a list of unique values in the 'group' column.
        
        :param df: Input DataFrame
        :param group: Column name to get unique values from
        :param group_by: Column name to sort the DataFrame by
        :param ascending: Boolean indicating the sorting order; True for ascending, False for descending; default is True
        :return: List of unique values in the 'group' column, sorted by the 'group_by' column
        """
        sorted_df = df.sort_values(by=group_by, ascending=ascending)
        unique_values = pd.Series(sorted_df[group].unique()).tolist()
        return unique_values
    
    #DATES/TIMES
    def dates_set_column(df: pd.DataFrame, date_column='date', date_index=False) -> pd.DataFrame:
        """
        Converts the specified date column to datetime objects, sorts the DataFrame by date, and optionally sets the date column as the index.
        
        :param df: Input DataFrame with a date column
        :param date_column: Name of the date column; default is 'date'
        :param date_index: Boolean indicating whether to set the date column as the index; default is False
        :return: DataFrame with the date column converted to datetime objects and sorted by date
        """
        df[date_column] = pd.to_datetime(df[date_column], dayfirst=True)
        df.sort_values(by=date_column, inplace=True)
        
        if date_index:
            df.set_index(date_column, inplace=True)
        else:
            df.reset_index(inplace=True, drop=True)
        
        return df
    
    def dates_split(df: pd.DataFrame, date_column='date', format='period') -> pd.DataFrame:
        """
        Splits the specified date column into different date components (tax year, year, quarter, month, week, day, and weekday) and adds them as new columns to the DataFrame.

        :param df: Input DataFrame with a date column
        :param date_column: Name of the date column; default is 'date'
        :param format: Format of the date components ('period', 'numeric', 'named_period', or 'named_numeric'); default is 'period'
        :return: DataFrame with new date component columns added
        """
        def get_date_columns(format) -> dict:
            if format in ['period', 'numeric']:
                year = df[date_column].dt.year if format == 'numeric' else pd.to_datetime(df[date_column]).dt.to_period('Y')
                quarter = df[date_column].dt.quarter if format == 'numeric' else pd.to_datetime(df[date_column]).dt.to_period('Q')
                month = df[date_column].dt.month if format == 'numeric' else pd.to_datetime(df[date_column]).dt.to_period('M')
            else:
                year = df[date_column].dt.year
                quarter = df[date_column].dt.quarter
                month = df[date_column].dt.month_name()

            return {
                'tax year': tax.tax_year(df),
                'year': year,
                'quarter': quarter,
                'month': month,
                'week': df[date_column].dt.isocalendar().week,
                'day': df[date_column].dt.day,
                'weekday': df[date_column].dt.weekday if format in ['period', 'numeric'] else df[date_column].dt.day_name()
            }

        new_columns = get_date_columns(format)

        for column_name, column_values in new_columns.items():
            df.insert(loc=1, column=column_name, value=column_values)

        return df

    def dates_create_range(first_date, last_date="today", split_dates=True, split_format='named_numeric', date_index=False) -> pd.DataFrame:
        """
        Creates a DataFrame containing a date range between first_date and last_date, with optional date component columns and date index.

        :param first_date: First date of the date range
        :param last_date: Last date of the date range; default is "today"
        :param split_dates: Boolean indicating whether to add date component columns; default is True
        :param split_format: Format of the date components if split_dates is True ('period', 'numeric', 'named_period', or 'named_numeric'); default is 'named_numeric'
        :param date_index: Boolean indicating whether to set the date column as the index; default is False
        :return: DataFrame containing the date range with optional date component columns and date index
        """
        dates = pd.date_range(first_date, pd.to_datetime(last_date))
        date_range = pd.DataFrame(dates, columns=['date'])
        date_range['date'] = pd.to_datetime(date_range['date'])

        if date_index:
            date_range.set_index('date', inplace=True)

        if split_dates:
            date_range = split_dates(date_range, format=split_format)

        return date_range

    def dates_filter_range(data: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
        """
        Filters the input DataFrame based on the given start_date and end_date. Assumes the DataFrame has a DateTimeIndex.

        :param data: Input DataFrame with a DateTimeIndex
        :param start_date: Start date for filtering
        :param end_date: End date for filtering
        :return: Filtered DataFrame containing only rows within the specified date range
        """
        date_range = (data.index > start_date) & (data.index <= end_date)
        return data[date_range]
    
    def dates_fill_gaps(df: pd.DataFrame, date_column: str = 'date') -> pd.DataFrame:
        """
        Fill missing dates in the DataFrame with empty rows.

        :param df: Input DataFrame with a date column
        :param date_column: Column name containing dates; default is 'date'
        :return: DataFrame with missing dates filled
        """
        first_date = df[date_column].min()
        last_date = df[date_column].max()
        date_range = pd.date_range(start=first_date, end=last_date)

        df.set_index(date_column, inplace=True)

        df = df.reset_index()
        df["count"] = df.groupby(date_column).cumcount()
        df.set_index([date_column, "count"], inplace=True)

        date_range = pd.MultiIndex.from_product([pd.date_range(start=first_date, end=last_date), range(df.index.levels[1].size)])

        df_filled = df.reindex(date_range)
        df_filled.reset_index(inplace=True)
        df_filled.rename(columns={'level_0': date_column}, inplace=True)
        df_filled.drop(columns=['level_1'], inplace=True)

        return df_filled


    #METRICS
    def metric_columns(df: pd.DataFrame, metric: str = 'sum') -> pd.DataFrame:
        """
        Calculate the specified metric for all numerical columns in a DataFrame.

        :param df: Input DataFrame
        :param metric: Desired metric to calculate ('sum', 'mean', 'max', 'min', 'std', 'var', 'mode', 'count')
        :return: DataFrame with the calculated metric for all numerical columns
        """
        metric_func = {
            'sum': df.sum(),
            'mean': df.mean(),
            'max': df.max(),
            'min': df.min(),
            'std': df.std(),
            'var': df.var(),
            'mode': df.mode().iloc[0],
            'count': df.count(),
        }
        result = metric_func[metric]
        return pd.DataFrame(result).reset_index().rename(columns={0: metric, "index": "column"})

    #CASH
    def gross_profit(df: pd.DataFrame, group_by: str, columns: str = 'r-e-p', custom_columns: list = None) -> pd.DataFrame:
        """
        Calculate gross profit metrics for a DataFrame based on the specified columns.

        :param df: Input DataFrame with required columns
        :param group_by: Column name to group by
        :param columns: A string indicating which set of columns to use ('r-e-p' or 'custom'); default is 'r-e-p'
        :param custom_columns: A list of custom column names to use if 'custom' is selected; default is None
        :return: DataFrame with gross profit metrics
        """
        column_set = {'r-e-p': ['revenue', 'expenditure', 'gross profit'],
                    'custom': custom_columns if custom_columns else []}

        columns_to_keep = column_set[columns]
        columns_to_keep.insert(0, group_by)
        df = df[columns_to_keep]

        metrics = {'sum': df.groupby(df[group_by]).sum(),
                'mean': df.groupby(df[group_by]).mean(),
                'max': df.groupby(df[group_by]).max(),
                'min': df.groupby(df[group_by]).min(),
                'count': df.groupby(df[group_by]).count().astype(int)}

        df = metrics['sum']
        return df
    
    def cash_cumulate(df: pd.DataFrame, expenditure: bool = True, revenue: bool = True, profit: bool = True, gross_return: bool = True) -> pd.DataFrame:
        """
        Calculate cumulative revenue, expenditure, profit, and gross return for a DataFrame.

        :param df: Input DataFrame with columns named 'Expenditure', 'Revenue', 'Gross Profit', and 'Gross Return (%)'
        :param expenditure: Calculate cumulative expenditure if True; default is True
        :param revenue: Calculate cumulative revenue if True; default is True
        :param profit: Calculate cumulative profit if True; default is True
        :param gross_return: Calculate gross return if True; default is True
        :return: DataFrame with calculated cumulative columns
        """
        if revenue:
            df["cumulative revenue"] = df["revenue"].cumsum()
        if expenditure:
            df["cumulative expenditure"] = df["expenditure"].cumsum()
        if profit:
            df["cumulative profit"] = df["cumulative revenue"] - df["cumulative expenditure"]
        if gross_return:
            df["gross return (%)"] = df["cumulative profit"] / df["cumulative expenditure"] * 100
            df["gross return (%)"] = df["gross return (%)"].fillna(0)

        return df
    
    #AGGREGATE
    def aggregate_category(df, group_by, column_name, number_column, order_list, metric='sum', subgroup_column=None) -> pd.DataFrame:
        """
        Aggregate a DataFrame by the specified metric for each category in the order_list, with an optional subgroup column.
        
        :param df: DataFrame to be aggregated
        :param group_by: Column name to group by
        :param column_name: Column name containing categories
        :param number_column: Column name with numerical data to perform aggregation
        :param order_list: List of categories in the desired order for the output DataFrame
        :param metric: Aggregation metric ('sum', 'mean', 'max', 'min', or 'count'); default is 'sum'
        :param subgroup_column: Optional column name for sub-grouping, default is None
        :return: Aggregated DataFrame with one column per category in order_list
        """
        if metric not in ['sum', 'mean', 'max', 'min', 'count']:
            raise ValueError("Invalid metric. Must be one of 'sum', 'mean', 'max', 'min', or 'count'.")

        aggregated_data = []
        for category in order_list:
            subset = df.loc[df[column_name] == category]
            
            if subgroup_column:
                group_columns = [df[group_by], df[subgroup_column]]
            else:
                group_columns = df[group_by]
                
            aggregation_methods = {
                'sum': subset.groupby(group_columns)[number_column].sum(),
                'mean': subset.groupby(group_columns)[number_column].mean(),
                'max': subset.groupby(group_columns)[number_column].max(),
                'min': subset.groupby(group_columns)[number_column].min(),
                'count': subset.groupby(group_columns)[number_column].count().astype(int)
            }
            
            aggregated_subset = aggregation_methods[metric]
            aggregated_data.append(aggregated_subset.rename(category))

        result_df = pd.concat(aggregated_data, axis=1)
        result_df = result_df.fillna(0)
        result_df = result_df.sort_values(by=group_by)
        return result_df
    
    def graph_index_columns(df: pd.DataFrame, colors: str = 'one', barmode: str = 'group') -> go.Figure:
        """
        Creates a grouped bar chart using a DataFrame with a PeriodIndex (specifically for monthly periods) or other index types.

        :param df: Input DataFrame with index and columns to be used for the bar chart
        :param colors: Color set to use for the bars; default is 'one'
        :param barmode: Barmode for the plotly chart; default is 'group'
        :return: plotly.graph_objects.Figure containing the bar chart
        """
        if df.index.dtype == 'period[M]':
            df.index = df.index.strftime("%Y-%m").to_list()

        col_names = df.columns.values.tolist()
        index_names = df.index.values.tolist()
        index_names = list(map(str, index_names))

        colors = NarcoAnalytics.color_list(col_names, colors=colors)
        bars = []

        for i in col_names:
            bar = go.Bar(name=i, x=index_names, y=df[i], marker_color=colors[col_names.index(i)])
            bars.append(bar)

        fig = go.Figure(bars)
        fig.update_layout(barmode=barmode)

        return fig
    
    def graph_metrics(df: pd.DataFrame, graph_type: str = 'bar', colors: str = 'one') -> go.Figure:
        """
        Creates a bar or pie chart using a DataFrame with index and values.

        :param df: Input DataFrame with index and values to be used for the chart
        :param graph_type: Type of chart to create, either 'bar' or 'pie'; default is 'bar'
        :param colors: Color set to use for the bars or pie slices; default is 'one'
        :return: plotly.graph_objects.Figure containing the chart
        """
        names = df['column'].tolist()
        values = df['sum'].tolist()
        colors = NarcoAnalytics.color_list(values, colors='one')

        fig_data = {
            'pie': go.Pie(labels=names, values=values, marker_colors=colors, sort=False),
            'bar': go.Bar(x=names, y=values, marker_color=colors)
        }

        fig = go.Figure(data=fig_data[graph_type])

        return fig