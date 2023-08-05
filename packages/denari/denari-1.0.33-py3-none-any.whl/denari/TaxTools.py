import os
import pandas as pd
import numpy as np
import datetime as dt

class TaxTools():
    def tax_year(df, country_code='uk'):
        """
        Creates a tax year pd.Series based on the provided DataFrame and country_code.
        
        :param df: DataFrame containing a 'date' column with datetime objects
        :param country_code: Two-letter country code ('uk' or 'usa') for tax year calculation; default is 'uk'
        :return: pd.Series with tax year values corresponding to each date in the input DataFrame
        """
        tax_year_start_end = {
            'uk': {'start': '4-6', 'end': '4-5'},
            'usa': {'start': '1-1', 'end': '12-31'}
        }
        
        if country_code not in tax_year_start_end:
            raise ValueError("Invalid country code. Must be 'uk' or 'usa'.")

        dff = df.loc[:, ['date']].copy()
        start = tax_year_start_end[country_code]['start']
        
        dff['year'] = dff['date'].dt.year
        dff['start_date'] = pd.to_datetime(dff['year'].astype(str) + '-' + start)
        
        dff['before_start'] = dff['date'] < dff['start_date']
        dff['year_before'] = dff['year'] - 1
        dff['year_after'] = dff['year'] + 1
        
        dff['tax_year'] = np.where(
            dff['before_start'],
            dff['year_before'].astype(str) + '/' + dff['year'].astype(str),
            dff['year'].astype(str) + '/' + dff['year_after'].astype(str)
        )
        return dff['tax_year']

    def get_law(tax_name: str, tax_year: str = '2021/2022') -> pd.DataFrame:
        """
        Get tax law data for the given tax_name and tax_year.

        Args:
            tax_name (str): Tax law name. Options for UK tax_name:
                - 'income tax'
                - 'employee ni'
                - 'corporate ni'
                - 'dividend rates'
                - 'student loans'
                - 'corporation tax'
                - 'employee ni bands'
                - 'corporate ni bands'
                - 'high income threshold'
                - 'dividend tax free allowance'
            tax_year (str): Tax year. Options are '2021/2022' and '2022/2023'. Default is '2021/2022'.

        Returns:
            pd.DataFrame: Tax law data as a DataFrame.
        """
        path = os.path.dirname(__file__)
        log_folder = os.path.join(path, 'UK Tax Tables')
        tax_table_log = pd.read_csv(os.path.join(log_folder, 'tax_name_log.csv'))
        year = tax_table_log.loc[tax_table_log['tax name'] == tax_name, tax_year].item()
        tax = tax_table_log.loc[tax_table_log['tax name'] == tax_name, 'filename'].item()
        file_path = os.path.join(log_folder, year, tax)
        tax_data = pd.read_csv(file_path)
        return tax_data

    #Universal Tax Tools LEVEL 0
    def create_table(tax_rates: pd.DataFrame) -> pd.DataFrame:
        """
        Create a tax rate table with threshold minimum, threshold maximum, and rate.

        Args:
            tax_rates (pd.DataFrame): DataFrame containing tax rates with a 'threshold min' column.

        Returns:
            pd.DataFrame: A new DataFrame with 'threshold min', 'threshold max', and 'rate' columns.
        """
        modified_tax_rates = tax_rates.copy()
        modified_tax_rates['threshold max'] = modified_tax_rates['threshold min'].shift(-1)
        modified_tax_rates = modified_tax_rates[['threshold min', 'threshold max', 'rate']]
        modified_tax_rates = modified_tax_rates.fillna(np.inf)
        return modified_tax_rates

    def marginal(cash: float, tax_table: pd.DataFrame) -> float:
        """
        Calculate the marginal tax based on the given cash and tax rate table.

        Args:
            cash (float): The cash amount to calculate the marginal tax for.
            tax_table (pd.DataFrame): DataFrame containing tax rates with 'threshold min', 'threshold max', and 'rate' columns.

        Returns:
            float: The total marginal tax for the given cash amount.
        """
        modified_tax_table = tax_table.copy()
        modified_tax_table.loc[-1] = [cash, cash, np.NaN]
        modified_tax_table.index = modified_tax_table.index + 1
        modified_tax_table = modified_tax_table.sort_index()
        modified_tax_table = modified_tax_table.sort_values(by=['threshold min'])
        modified_tax_table['threshold max'] = modified_tax_table['threshold max'].sort_values().values
        modified_tax_table = modified_tax_table.reset_index(drop=True)
        cut = modified_tax_table.index[modified_tax_table['threshold max'] == cash].tolist()
        cut = cut[0]
        modified_tax_table = modified_tax_table[modified_tax_table.index <= cut].copy()
        modified_tax_table['tax'] = (modified_tax_table['threshold max'] - modified_tax_table['threshold min']) * modified_tax_table['rate']
        total_tax = modified_tax_table['tax'].sum()
        return total_tax

    def marginalise(cash: float, table: pd.DataFrame) -> float:
        """
        Calculate the marginal tax for a given cash amount using the provided tax rate table.

        Args:
            cash (float): The cash amount to calculate the marginal tax for.
            table (pd.DataFrame): DataFrame containing tax rates.

        Returns:
            float: The total marginal tax for the given cash amount.
        """
        created_table = TaxTools.create_table(table)
        total_tax = TaxTools.marginal(cash, created_table)
        return total_tax

    def replace_threshold_rates(threshold_table: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame:
        """
        Replace the tax rates in the threshold table with the rates provided in the rates DataFrame.

        Args:
            threshold_table (pd.DataFrame): DataFrame containing the tax thresholds.
            rates (pd.DataFrame): DataFrame containing the tax rates to be replaced.

        Returns:
            pd.DataFrame: DataFrame containing the tax thresholds with updated tax rates.
        """
        updated_table = threshold_table.copy()
        new_rates = rates.copy()
        updated_table['rate'] = new_rates['rate']
        return updated_table

    def interpret_single_df_value(df: pd.DataFrame) -> int:
        """
        Interpret the single value from a DataFrame with a column named 'value'.

        Args:
            df (pd.DataFrame): DataFrame containing a single value in the 'value' column.

        Returns:
            int: The single value in the 'value' column as an integer.
        """
        return int(df['value'].iloc[0])

    def optimal_iterations(input_value: int) -> int:
        """
        Find the optimal number of iterations for a given input value.

        Args:
            input_value (int): The input value to calculate the optimal number of iterations.

        Returns:
            int: The optimal number of iterations.
        """
        x_min = 1
        x_max = input_value / 2
        d = {}

        for i in range(int(x_min), int(x_max) + 1):
            key = i
            value = int((input_value / i) + i)
            d[key] = value + int(input_value / i)

        min_value = min(d.values())
        min_key = min(k for k, v in d.items() if v == min_value)
        return min_key

    #UK Tax Tools LEVEL 1
    def interpret_tax_code_allowance(tax_code: str) -> int:
        """
        Extract the tax allowance from a given tax code.

        Args:
            tax_code (str): The tax code as a string (e.g., '1257A').

        Returns:
            int: The tax allowance as an integer (e.g., 1257).
        """
        allowance = int(''.join(char for char in tax_code if char.isdigit())) * 10
        return allowance

    def interpret_tax_code_ni_band(tax_code: str) -> str:
        """
        Extract the National Insurance (NI) band from a given tax code.

        Args:
            tax_code (str): The tax code as a string (e.g., '1257A').

        Returns:
            str: The NI band as a string (e.g. 'A').
        """
        ni_band = ''.join(char for char in tax_code if not char.isdigit())
        return ni_band

    def adjust_allowance(salary: float, tax_allowance: float, tax_table: pd.DataFrame, tax_year: str) -> pd.DataFrame:
        """
        Adjust the tax allowance based on the given salary and tax year.

        Args:
            salary (float): The salary of the individual.
            tax_allowance (float): The initial tax allowance.
            tax_table (pd.DataFrame): The tax table with threshold and rate values.
            tax_year (str): The tax year for which the allowance adjustment is required.

        Returns:
            pd.DataFrame: The adjusted tax table.
        """
        a = tax_table.copy()
        allowance_reduction = a.loc[1, 'threshold min'] - tax_allowance
        a.loc[1, 'threshold min'] -= allowance_reduction
        a.loc[2, 'threshold min'] -= allowance_reduction

        high_income_threshold = TaxTools.get_law('high income threshold', tax_year)
        high_income_value = TaxTools.interpret_single_df_value(high_income_threshold)

        if salary > high_income_value:
            change_range = high_income_value + 2 * tax_allowance
            change_df = pd.DataFrame({'numbers': list(range(high_income_value, change_range + 1, 2))})
            change_df = change_df[change_df['numbers'] <= salary]
            allowance_chg = change_df.index[-1]
        else:
            allowance_chg = 0

        a.loc[1, 'threshold min'] -= allowance_chg
        a.loc[2, 'threshold min'] -= allowance_chg

        return a

    def adjust_ni_band(tax_table: pd.DataFrame, ni_band_table: pd.DataFrame, ni_band: str) -> pd.DataFrame:
        """
        Adjust the National Insurance (NI) band rates in the tax table based on the given NI band.

        Args:
            tax_table (pd.DataFrame): The tax table with threshold and rate values.
            ni_band_table (pd.DataFrame): The NI band table with category and rate values.
            ni_band (str): The NI band category to adjust the rates for.

        Returns:
            pd.DataFrame: The adjusted tax table with updated NI band rates.
        """
        selected_ni_band = ni_band_table[ni_band_table['category'] == ni_band]
        transposed_ni_band = selected_ni_band.transpose()
        transposed_ni_band.columns = ['rate']
        transposed_ni_band.reset_index(drop=True, inplace=True)
        transposed_ni_band.drop([0], axis=0, inplace=True)
        transposed_ni_band.reset_index(drop=True, inplace=True)

        adjusted_tax_table = tax_table.copy()
        adjusted_tax_table['rate'] = transposed_ni_band['rate']

        return adjusted_tax_table

    def create_dividend_table(salary: float, tax_free_amount: float, tax_table: pd.DataFrame) -> pd.DataFrame:
        """
        Create a dividend tax table by adjusting the given tax_table based on salary and tax-free amount.

        Args:
            salary (float): The salary amount.
            tax_free_amount (float): The tax-free amount for dividend income.
            tax_table (pd.DataFrame): The tax table with threshold and rate values.

        Returns:
            pd.DataFrame: The adjusted tax table for dividend income.
        """
        adjusted_tax_table = tax_table.copy()
        adjusted_tax_table.loc[-1] = [salary + tax_free_amount, np.NaN]
        adjusted_tax_table.sort_values(by=['threshold min'], inplace=True)
        adjusted_tax_table.reset_index(drop=True, inplace=True)
        adjusted_tax_table.fillna(method='ffill', inplace=True)
        
        cut_idx = adjusted_tax_table.index[adjusted_tax_table['threshold min'] == salary + tax_free_amount].tolist()
        cut_idx = cut_idx[0]
        dividend_table = adjusted_tax_table[adjusted_tax_table.index >= cut_idx]

        return dividend_table

    def create_student_loan_table(table: pd.DataFrame, plan: str) -> pd.DataFrame:
        """
        Create a student loan repayment table by filtering the given table based on the repayment plan.

        Args:
            table (pd.DataFrame): The table containing student loan repayment information for multiple plans.
            plan (str): The student loan repayment plan to filter the table.

        Returns:
            pd.DataFrame: The filtered student loan repayment table for the specified plan.
        """
        filtered_table = table[table['category'] == plan]
        student_loan_table = filtered_table[['threshold min', 'rate']]

        return student_loan_table

    #UK Tax Laws LEVEL 2
    def employee_ni(salary: float, tax_year: str, tax_code: str) -> float:
        """
        Calculate the employee's National Insurance (NI) contribution based on their salary, tax year, and tax code.

        Args:
            salary (float): The employee's salary.
            tax_year (str): The tax year for which the NI contribution is to be calculated.
            tax_code (str): The employee's tax code, used to determine the NI band.

        Returns:
            float: The calculated employee's NI contribution.
        """
        ni_rates = TaxTools.get_law('employee ni', tax_year)
        ni_band = TaxTools.interpret_tax_code_ni_band(tax_code)
        ni_bands = TaxTools.get_law('employee ni bands', tax_year)
        adjusted_ni_rates = TaxTools.adjust_ni_band(ni_rates, ni_bands, ni_band)
        ni_contribution = TaxTools.marginalise(salary, adjusted_ni_rates)

        return ni_contribution

    def income_tax(salary: float, tax_year: str, tax_code: str) -> float:
        """
        Calculate the income tax for an employee based on their salary, tax year, and tax code.

        Args:
            salary (float): The employee's salary.
            tax_year (str): The tax year for which the income tax is to be calculated.
            tax_code (str): The employee's tax code, used to determine the tax-free allowance.

        Returns:
            float: The calculated income tax.
        """
        income_tax_rates = TaxTools.get_law('income tax', tax_year)
        tax_free_allowance = TaxTools.interpret_tax_code_allowance(tax_code)
        adjusted_income_tax_rates = TaxTools.adjust_allowance(salary, tax_free_allowance, income_tax_rates, tax_year)
        income_tax_amount = TaxTools.marginalise(salary, adjusted_income_tax_rates)

        return income_tax_amount
    
    def corporate_ni(salary: float, tax_year: str, tax_code: str) -> float:
        """
        Calculate the corporate National Insurance (NI) for an employee based on their salary, tax year, and tax code.

        Args:
            salary (float): The employee's salary.
            tax_year (str): The tax year for which the corporate NI is to be calculated.
            tax_code (str): The employee's tax code, used to determine the NI band.

        Returns:
            float: The calculated corporate NI.
        """
        corporate_ni_rates = TaxTools.get_law('corporate ni', tax_year)
        corporate_ni_bands = TaxTools.get_law('corporate ni bands', tax_year)
        ni_band = TaxTools.interpret_tax_code_ni_band(tax_code)
        adjusted_corporate_ni_rates = TaxTools.adjust_ni_band(corporate_ni_rates, corporate_ni_bands, ni_band)
        corporate_ni_amount = TaxTools.marginalise(salary, adjusted_corporate_ni_rates)

        return corporate_ni_amount

    def corporation_tax(gross_profit: float, tax_year: str) -> float:
        """
        Calculate the corporation tax for a company based on the gross profit and tax year.

        Args:
            gross_profit (float): The company's gross profit.
            tax_year (str): The tax year for which the corporation tax is to be calculated.

        Returns:
            float: The calculated corporation tax.
        """
        corporation_tax_rates = TaxTools.get_law('corporation tax', tax_year)
        corporation_tax_amount = TaxTools.marginalise(gross_profit, corporation_tax_rates)

        return corporation_tax_amount

    def dividend_tax(salary: float, dividend: float, tax_year: str, tax_code: str) -> float:
        """
        Calculate the dividend tax based on the salary, dividend, tax year, and tax code.

        Args:
            salary (float): The individual's salary.
            dividend (float): The dividend income received.
            tax_year (str): The tax year for which the dividend tax is to be calculated.
            tax_code (str): The individual's tax code.

        Returns:
            float: The calculated dividend tax.
        """
        income_tax_rates = TaxTools.get_law('income tax', tax_year)
        tax_allowance = TaxTools.interpret_tax_code_allowance(tax_code)
        adjusted_income_tax_rates = TaxTools.adjust_allowance(salary, tax_allowance, income_tax_rates, tax_year)
        
        dividend_rates = TaxTools.get_law('dividend rates', tax_year)
        adjusted_dividend_rates = TaxTools.replace_threshold_rates(adjusted_income_tax_rates, dividend_rates)
        
        tax_free_allowance_df = TaxTools.get_law('dividend tax free allowance', tax_year)
        tax_free_allowance = TaxTools.interpret_single_df_value(tax_free_allowance_df)
        
        dividend_table = TaxTools.create_dividend_table(salary, tax_free_allowance, adjusted_dividend_rates)
        total_income = salary + dividend
        
        dividend_tax_amount = TaxTools.marginalise(total_income, dividend_table)

        return dividend_tax_amount

    def student_loans(cash: float, plan: str, tax_year: str) -> float:
        """
        Calculate student loan repayment based on the cash amount, plan, and tax year.

        Args:
            cash (float): The cash amount to be considered for student loan repayment calculation.
            plan (str): The student loan repayment plan type (e.g., 'Plan 1', 'Plan 2', or 'Plan 4').
            tax_year (str): The tax year for which the student loan repayment is to be calculated.

        Returns:
            float: The calculated student loan repayment.
        """
        student_loan_df = TaxTools.get_law('student loans', tax_year)
        student_loan_table = TaxTools.create_student_loan_table(student_loan_df, plan)
        student_loan_repayment = TaxTools.marginalise(cash, student_loan_table)

        return student_loan_repayment

    #UK Tax Calculation LEVEL 3
    def salary_taxes(salary: float, tax_code: str, student_loan_plan: str, tax_year: str, student_loan_second_plan: str = 'plan 0') -> pd.DataFrame:
        """
        Calculate various taxes for a given salary, tax code, and student loan plans in a specified tax year.

        Args:
            salary (float): The employee's salary.
            tax_code (str): The employee's tax code.
            student_loan_plan (str): The employee's primary student loan repayment plan type.
            tax_year (str): The tax year for which the taxes are to be calculated.
            student_loan_second_plan (str, optional): The employee's secondary student loan repayment plan type, if any. Defaults to 'plan 0'.

        Returns:
            pd.DataFrame: A DataFrame containing the calculated taxes and other relevant information.
        """
        employee_ni = TaxTools.employee_ni(salary, tax_year, tax_code)
        income_tax = TaxTools.income_tax(salary, tax_year, tax_code)
        corporate_ni = TaxTools.corporate_ni(salary, tax_year, tax_code)
        student_loans_primary = TaxTools.student_loans(salary, student_loan_plan, tax_year)
        student_loans_secondary = TaxTools.student_loans(salary, student_loan_second_plan, tax_year)
        
        total_student_loans = student_loans_primary + student_loans_secondary
        salary_takehome = salary - employee_ni - income_tax - total_student_loans
        total_employee_cost = salary + corporate_ni
        
        tax_data = {
            'Salary': [salary],
            'Employee National Insurance': [employee_ni],
            'Income Tax': [income_tax],
            'Employer National Insurance': [corporate_ni],
            'Student Loans': [total_student_loans],
            'Salary Takehome': [salary_takehome],
            'Total Employee Cost': [total_employee_cost]
        }
        
        return pd.DataFrame(data=tax_data)

    #UK Tax Corporate Calculation LEVEL 4
    def ltd_full_take(turnover: float, salary: float, expenses: float, tax_year: str, tax_code: str, student_loan_plan: str = 'plan 0', student_loan_second_plan: str = 'plan 0') -> pd.DataFrame:
        """
        Calculate the total take-home for a limited company owner, given turnover, salary, expenses, tax year, tax code, and student loan plans.

        Args:
            turnover (float): The company's turnover.
            salary (float): The owner's salary.
            expenses (float): The company's expenses.
            tax_year (str): The tax year for which the calculations are to be done.
            tax_code (str): The owner's tax code.
            student_loan_plan (str, optional): The owner's primary student loan repayment plan type. Defaults to 'plan 0'.
            student_loan_second_plan (str, optional): The owner's secondary student loan repayment plan type, if any. Defaults to 'plan 0'.

        Returns:
            pd.DataFrame: A DataFrame containing the calculated take-home and other relevant information.
        """
        salary_taxes = TaxTools.salary_taxes(salary, tax_code, 'plan 0', tax_year).copy()
        turnover_minus_expenses = turnover - expenses
        gross_profit = turnover - expenses - salary - TaxTools.corporate_ni(salary, tax_year, tax_code)
        
        corp_tax = TaxTools.corporation_tax(gross_profit, tax_year)
        net_profit = gross_profit - corp_tax
        gross_take = salary + net_profit
        
        dividend_tax = TaxTools.dividend_tax(salary, net_profit, tax_year, tax_code)
        dividend_takehome = net_profit - dividend_tax
        
        primary_student_loans = TaxTools.student_loans(gross_take, student_loan_plan, tax_year)
        secondary_student_loans = TaxTools.student_loans(gross_take, student_loan_second_plan, tax_year)
        total_student_loans = primary_student_loans + secondary_student_loans
        
        salary_taxes['Student Loans'] = total_student_loans
        total_takehome = int(salary_taxes['Salary Takehome']) + dividend_takehome - total_student_loans
        percentage_take = total_takehome / turnover * 100
        
        additional_data = {
            'Usable Funds': [turnover_minus_expenses],
            'Corporation Tax': [corp_tax],
            'Dividend': [net_profit],
            'Dividend Tax': [dividend_tax],
            'Dividend Takehome': [dividend_takehome],
            'Gross Take': [gross_take],
            'Total Takehome': [total_takehome],
            'Percentage Take': [percentage_take]
        }
        
        additional_df = pd.DataFrame(additional_data)
        salary_taxes = salary_taxes.join(additional_df)
        
        return salary_taxes

    #UK Tax Corporate Scenario Iteration LEVEL 5

    def optimal_take(options: pd.DataFrame) -> pd.DataFrame:
        """
        Find the optimal take-home value from a given DataFrame containing different scenarios.

        Args:
            options (pd.DataFrame): A DataFrame containing different scenarios with a 'Total Takehome' column.

        Returns:
            pd.DataFrame: A DataFrame containing the optimal take-home scenario(s) with the highest take-home value.
        """
        optimal_scenario = options[options['Total Takehome'] == options['Total Takehome'].max()]
        return optimal_scenario
    
    def iterate_salaries(turnover: float, min_salary: int, max_salary: int, expenses: float, tax_year: str, tax_code: str = '1257A', student_loan_plan: str = 'plan 0', student_loan_second_plan: str = 'plan 0', iteration_step: int = 1) -> pd.DataFrame:
        """
        Iterate through different salary levels within the given range and calculate the total take-home for a limited company owner.

        Args:
            turnover (float): The company's turnover.
            min_salary (int): The minimum salary to start iterating from.
            max_salary (int): The maximum salary to iterate up to.
            expenses (float): The company's expenses.
            tax_year (str): The tax year for which the calculations are to be done.
            tax_code (str, optional): The owner's tax code. Defaults to '1257A'.
            student_loan_plan (str, optional): The owner's primary student loan repayment plan type. Defaults to 'plan 0'.
            student_loan_second_plan (str, optional): The owner's secondary student loan repayment plan type, if any. Defaults to 'plan 0'.
            iteration_step (int, optional): The step size for iterating through salary levels. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing the calculated take-home and other relevant information for each salary level within the given range.
        """
        results = pd.DataFrame()

        for salary in range(min_salary, max_salary + 1, iteration_step):
            salary_data = TaxTools.ltd_full_take(turnover, salary, expenses, tax_year, tax_code, student_loan_plan, student_loan_second_plan)
            results = pd.concat([results, salary_data])

        results = results.reset_index(drop=True)

        return results

    def iterate_full_take(turnover: float, expenses: float, tax_year: str, tax_code: str = '1257A', student_loan_plan: str = 'plan 0', student_loan_second_plan: str = 'plan 0', optimal: bool = True) -> pd.DataFrame:
        """
        Iterate through different salary levels from 0 up to the turnover value minus expenses and calculate the total take-home for a limited company owner.

        Args:
            turnover (float): The company's turnover.
            expenses (float): The company's expenses.
            tax_year (str): The tax year for which the calculations are to be done.
            tax_code (str, optional): The owner's tax code. Defaults to '1257A'.
            student_loan_plan (str, optional): The owner's primary student loan repayment plan type. Defaults to 'plan 0'.
            student_loan_second_plan (str, optional): The owner's secondary student loan repayment plan type, if any. Defaults to 'plan 0'.

        Returns:
            pd.DataFrame: A DataFrame containing the calculated take-home and other relevant information for each salary level from 0 up to the turnover value minus expenses.
        """
        turnover_deduct_expenses = turnover - expenses
        results = TaxTools.iterate_salaries(turnover, 0, turnover_deduct_expenses, expenses, tax_year, tax_code, student_loan_plan, student_loan_second_plan, iteration_step=1)
       
        if optimal:
            results = TaxTools.optimal_take(results)

        return results

    #UK Tax Corporate Optimisation LEVEL 6

    def iterate_lite_full_take(turnover: float, expenses: float, tax_year: str, tax_code: str, student_loan_plan: str = 'plan 0', student_loan_second_plan: str = 'plan 0', optimal: bool = True) -> pd.DataFrame:
        """
        Optimise the take-home value for a limited company owner using a lighter approach.

        The function first finds an optimal range for iterating over different salary scenarios by using the optimal_iterations function. It then narrows down the range and iterates over the refined range to find the optimal take-home scenario.

        Args:
            turnover (float): The total turnover of the company.
            expenses (float): The total expenses of the company.
            tax_year (str): The tax year to consider for calculations (e.g., '2021/2022').
            tax_code (str): The tax code to use for calculations (e.g., '1257A').
            student_loan_plan (str, optional): The student loan plan to use for calculations (e.g., 'plan 1'). Defaults to 'plan 0'.
            student_loan_second_plan (str, optional): The second student loan plan to use for calculations (e.g., 'plan 2'). Defaults to 'plan 0'.

        Returns:
            pd.DataFrame: A DataFrame containing the optimal take-home scenario(s) with the highest take-home value.
        """
        turnover_deduct_expenses = turnover - expenses
        iteration_step = TaxTools.optimal_iterations(turnover_deduct_expenses)

        initial_scenarios = TaxTools.iterate_salaries(turnover, 0, turnover_deduct_expenses, expenses, tax_year, tax_code, student_loan_plan, student_loan_second_plan, iteration_step)
        optimal_row = initial_scenarios.index[initial_scenarios['Total Takehome'] == initial_scenarios['Total Takehome'].max()].tolist()
        optimal_range = [*range(optimal_row[0] - 1, optimal_row[0] + 2)]
        optimal_options = initial_scenarios.iloc[optimal_range]

        min_salary = int(optimal_options.iloc[[0]]['Salary'])
        max_salary = int(optimal_options.iloc[[2]]['Salary'])

        optimal_window = TaxTools.iterate_salaries(turnover, min_salary, max_salary, expenses, tax_year, tax_code, student_loan_plan, student_loan_second_plan, 1)
        results = pd.concat([initial_scenarios, optimal_window]).drop_duplicates().reset_index(drop=True)

        
        if optimal:
                results = TaxTools.optimal_take(results)

        return results