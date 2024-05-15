
import pandas as pd

def solution_1(Posts, Users):

    """ Input the solution here """
    # Łączenie ramek danych joinem
    merged_df = pd.merge(Users, Posts, left_on='Id', right_on='OwnerUserId')
    # filtruje wiersze aby wybrac odpowiednie
    merged_df = merged_df[merged_df['Location'] != '']
    # Grupowanie i zliczanie
    grouped_df = merged_df.groupby('Location').size().reset_index(name='Count')
    # Sortowanie i wybieranie 10 najczęściej występujących lokalizacji
    result_df = grouped_df.sort_values(by='Count', ascending=False).head(10)
    res = result_df.reset_index().iloc[:, [1, 2]]
    return res

def solution_2(Posts, PostLinks):
    """ Input the solution here """

    tmp1 = PostLinks.groupby('RelatedPostId').size().reset_index(name='NumLinks') \
        .rename(columns={"RelatedPostId": "PostId"})
    tmp2 = tmp1.merge(Posts, left_on="PostId", right_on="Id")
    tmp2 = tmp2.loc[tmp2.PostTypeId == 1]
    tmp3 = tmp2.loc[:, ["Title", "NumLinks"]] \
               .reset_index().iloc[:, [0, 1, 2]]
    result = tmp3.sort_values(by=["NumLinks", "index"], ascending=[False, True]) \
                 .iloc[:, [1, 2]].reset_index().iloc[:, [1, 2]]
    return result
    
def solution_3(Comments, Posts, Users):

    """ Input the solution here """
    tmp1 = Comments.groupby('PostId')['Score'].sum().reset_index() .rename(columns={"Score": "CommentsTotalScore"})
    tmp2 = Posts.merge(tmp1, left_on="Id", right_on="PostId")
    tmp3 = tmp2.loc[tmp2.PostTypeId == 1, ["OwnerUserId", "Title", "CommentCount", "ViewCount",
                                           "CommentsTotalScore"]]
    tmp4 = tmp3.merge(Users, left_on="OwnerUserId", right_on="Id")
    result = tmp4.sort_values(["CommentsTotalScore"], ascending=[False])
    result = result.loc[:, ["Title", "CommentCount", "ViewCount", "CommentsTotalScore",
                          "DisplayName", "Reputation", "Location"]].reset_index().iloc[:, [1, 2, 3, 4, 5, 6, 7]]
    result2 = result[0:10]
    return result2

def solution_4(Posts, Users):

    """ Input the solution here """
    tmp1 = Posts.loc[Posts.PostTypeId == 2,].groupby('OwnerUserId').size().reset_index(name='AnswersNumber')
    tmp2 = Posts.loc[Posts.PostTypeId == 1,].groupby('OwnerUserId').size().reset_index(name='QuestionsNumber')
    tmp3 = tmp1.merge(tmp2, left_on="OwnerUserId", right_on="OwnerUserId")
    tmp3 = tmp3.loc[tmp3.QuestionsNumber < tmp3.AnswersNumber,] \
            .sort_values(["AnswersNumber"], ascending=[False])
    tmp3 = tmp3[0:5]
    tmp4 = tmp3.merge(Users, left_on="OwnerUserId", right_on="Id") \
            .loc[:,["DisplayName", "QuestionsNumber", "AnswersNumber", "Location",
    "Reputation", "UpVotes", "DownVotes"]]
    return tmp4

def solution_5(Posts, Users):
    """ Input the solution here """
    tmp1 = Posts.loc[Posts.PostTypeId == 2]
    tmp1 = tmp1.groupby('ParentId').size().reset_index(name='AnswersCount')
    tmp2 = tmp1.merge(Posts, left_on="ParentId", right_on="Id")
    tmp2 = tmp2.loc[:, ["AnswersCount", "Id", "OwnerUserId"]]
    tmp3 = tmp2.merge(Users, left_on="OwnerUserId", right_on="AccountId")
    tmp4 = tmp3.groupby('AccountId').agg({
        'DisplayName': 'first',
        'Location': 'first',
        'AnswersCount': 'mean'
    }).reset_index()
    tmp5 = tmp4.rename(columns={"AnswersCount": "AverageAnswersCount"})
    tmp5 = tmp5.sort_values(["AverageAnswersCount", "AccountId"], ascending=[False, False]) \
               .reset_index().iloc[:, [1, 2, 3, 4]]
    result = tmp5[0:10]
    return result

