import pandas as pd


pd.options.display.width = 0
pd.options.display.max_colwidth = 0
pd.options.display.max_columns = 0
pd.options.display.max_rows = 150
pd.options.display.min_rows = 25
pd.options.display.show_dimensions = True

df = pd.read_csv('jeopardy.csv')
df.columns = ['Show Number', 'Air Date', 'Round', 'Category', 'Value', 'Question', 'Answer']
df.insert(5, 'Value Float', df['Value'].str.replace(r'[\$,]', '', regex=True).astype(float))


def search_string_column(data: pd.DataFrame, column: str, words: list, regex=True, case=True) -> pd.DataFrame:
    if regex:
        return data.loc[data[f'{column}'].str.contains(r''.join([rf"(?=.*\b{word}\b)" for word in words]),
                                                       regex=regex, case=case)]
    return data.loc[data[f'{column}'].str.contains(r' '.join(words), case=case)]


def unique_answer_counts(data):
    return data.Answer.value_counts()


data_from_1990s = df.loc[df['Air Date'].str.startswith('19')]
data_from_2000s = df.loc[df['Air Date'].str.startswith('20')]


def compare_two_data_by_column(data_1, data_2, column, words: list, case=False):
    data_a = search_string_column(data_1, column, words, case=case)
    data_b = search_string_column(data_2, column, words, case=case)
    return f"Number of Questions Containing {words} from the Dataframe 1: {data_a.count().max()}\n"\
           f"Number of Questions Containing {words} from the Dataframe 2: {data_b.count().max()}"


def column_relation(data: pd.DataFrame, columns: list, variable: str = None) -> pd.DataFrame:
    """Function takes a dataframe and '2' Columns
    \n-it uses 'groupby()' and value_counts() on the provided Columns
    \n-if a variable is provided it returns rows containing the provided variable
    \n-else it returns the whole dataframe"""
    column_a, column_b = columns[0], columns[1]
    filtered_data = data.groupby([column_a])[column_b].value_counts().reset_index()
    if variable:
        a = search_string_column(filtered_data, column_a, [variable], regex=True, case=False)
        b = search_string_column(filtered_data, column_b, [variable], regex=True, case=False)
        merged = pd.merge(a, b, how='outer')
        pivot = merged.pivot_table(columns='Round', index='Category', values='count')
        return pivot.fillna(0).astype(int).sort_values(by=pivot.columns[0], ascending=False)
    return filtered_data


def quiz(data):
    questions_answers = data[['Question', 'Answer']]
    while True:
        sample = questions_answers.sample()
        question = sample['Question'].to_string(header=False, index=False)
        answer = sample['Answer'].to_string(header=False, index=False)
        print('Question:')
        print(question)
        user = input('Please Answer:\n')
        print('The Correct Answer:')
        print(answer)
        print(user.lower() == answer.lower())
        again = input('Try Again? Y or N\n')
        if again in 'Nn':
            break


print(df)
