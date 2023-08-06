from typing import List

class Review:
    """Class to represent and save data of a Review"""

    def __init__(self,reviewerID:str,reviewerName:str=None,score:int=None,review:str=None):
        self.reviewerID = reviewerID
        self.reviewerName = reviewerName
        self.score = score
        self.review = review


    def header(self)->List[str]:
        """Returns atributes names in list format"""
        return ['Id','Name','Score','Review']
    
    def header_str(self,delim:str)->List[str]:
        """Returns atributes names in str format"""
        return f'Id{delim}Name{delim}Score{delim}Review'
    

    def dataset_line(self)->List[str]:
        """Returns a atributes in list format"""
        return [self.reviewerID,self.reviewerName,self.score,self.review]

    def dataset_line_str(self,delim:str)->str:
        """Returns a the atributes in str format"""
        return f'{self.reviewerID}{delim}{self.reviewerName}{delim}{self.score}{delim}{self.review}'

    def reviewerID(self)->str:
        return self.reviewerID

    def reviewerName(self)->str:
        return self.reviewerName

    def score(self)->int:
        return self.score
    
    def review(self)->str:
        return self.review
    
    def set_reviewerName(self,reviewerName):
        self.reviewerName = reviewerName

    def set_score(self,score):
        self.score = score

    def set_review(self,review):
        self.review = review
        

    def __str__(self,verbose:bool=False)->str:
        """Turn class into string representation"""
        text = f'''
          ________________________
        /
        | ID : {self.reviewerID}
        | Name : {self.reviewerName}
        | Score: {self.score}
        \__________________________
        '''
        if verbose:
            text += f'''
        Review:
        {self.review}
            '''
        return text