import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
from json import load



  

def multiturn_generate_content_witness_statements(witness_statements):
  vertexai.init(project="cambridge-law24cam-7858", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=["""You are a legal aid who help create summaries"""]
  )
  
  info = (model.generate_content(f"Here are the witness statements, can you summarise them: {witness_statements}"))

  return info.text

def multiturn_generate_content_pass_one(case, summary):
  vertexai.init(project="cambridge-law24cam-7858", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=["""You are a legal aid is rating if these documents are similar or not"""]
  )
  
  info = (model.generate_content(f"""We are given a case and we are currently evaluating case notes and witness statements for a project. When comparing these, we need to judge the similarity of these cases and if they can be used to build up an arguement.
                                  The case we are questioning is as follows: {case}
                                  The summary of our current statements  is as follows: {summary}

                                    Please reply with an integer answer of 
                                    
                                    "similarity_score" 

                                    Where  similarity score is an integer from 1 to 100 where 100 means they are very similar

"""))

  return info.text



generation_config = {
    "max_output_tokens": 100000,
    "temperature": 1,
    "top_p": 0.6,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# multiturn_generate_content()


if __name__ == '__main__':

    # text_info = get

    witness_message = """

TRADE MARKS ACT 1994 
 
IN THE MATTER OF 
Trade Mark application number 1234567 
in the name of Bloggins Ltd 
and  
opposition number 456789 by Mark Jonesi 
 
 
WITNESS STATEMENT 
 
1. I, Mark Jones, of 14 Acacia Avenue, London W32 1XY am the director of Bloggers 
plc, a position which I have held since 2010. The facts in this statement come from 
my personal knowledge or the records of my company and I am duly authorised to 
speak on my company’s behalf in the prosecution of this application.ii 
 
2. My company has been using its trade mark since March 2001, initially in its shop 
in Acacia Avenue but expanding online and to premises in Manchester in 2003, 
Leeds in 2003 and both Birmingham and Edinburgh in 2005.iii Attached at exhibit 
JS1 are press articles which discuss the opening of these shops. At exhibit JS2 I 
provide copies of advertisements which appeared in the press at the time to promote 
our shops’ opening.iv 
 
3. Although the business began by selling overcoats, by the time the Manchester 
shop opened we sold a wide variety of articles of clothing. Now shown to me is 
exhibit JS3, which shows archive prints from the relevant period (25 November 2012 
to 24 November 2017) of the clothing items available on our online site.v I confirm 
that the full range of items was also available in-store. The trade mark is clearly 
visible on the website. Exhibit JS3 also contains photographs of the labels attached 
to our products, which show the trade mark. These have been used throughout the 
relevant period.vi 
 
4. Evidence of the publicity my company and its trade mark have received is shown 
at exhibit JS4, in the form of articles which appeared in national newspapers and 
magazines in the relevant period, as well as advertisements placed by us. 
Advertising spend was roughly £350,000 in each year of the relevant period. 
Evidence of advertising breakdown by publication is at exhibit JS5.vii 
 
5. Turnover in the relevant period was as follows:  
2012/2013  £561,298 
2013/2014 £732,987 
2014/2015 £982,225 
2015/2016 £813,562 
2016/2017 £812,255 
 
6. Produced at exhibit JS5 is a selection of invoices dated within the relevant period 
which show sales of goods under our trade mark.viii 
 
7. The fact in this witness statement are true to the best of my knowledge and belief. 
 
SIGNED: 
 
 
DATED: 
 
 
 i Opposition and cancellation details only need to be provided if you are involved in tribunal proceedings. 
 ii The witness statement must be in the name of an individual, so it is important you say who is giving this 
evidence and where your information comes from. 
 iii The way in which you give information is not critical, as long as you explain the circumstances and try to 
support your claims (e.g. turnover figures) with documents (“exhibits”: see guidance notes). If you are bringing 
a claim under s. 3(6) (“bad faith”), you may not need to give details about sales like in this example but you 
should try to explain all the relevant facts regarding the filing of the trade mark, including, for example, why 
your interest in the mark is legitimate. Any documents you are able to provide to back up your claims should 
be filed as exhibits. 
 iv Providing independent evidence can help support your claims, particularly if it shows the range of 
goods/services you offered. Note how the documentary evidence (adverts) which supports the statements is 
introduced as exhibits. 
 v Evidence about how long the trade mark has been used and where it has been used (whether that is in a 
particular area or throughout the UK, or in the EU if it is an EU mark) is important.  
 vi It is important to make sure that you show which goods/services the trade mark has been used on, especially 
if you are applying for or relying on lots of different goods and services. Note how the witness confirms that 
the labels with the trade mark were used at the relevant time. 
 vii Press articles and adverts, as well as the amount spent on advertising, are helpful in showing how widely 
your mark has been publicised, especially if they were in national publications. 
 viii Invoices help support the claim to turnover made above. They sometimes also show the trade mark, the 
range of goods/services sold and how wide the geographical reach of the business is. 




    """

    nda = """

    
1
 
 
COMMITMENT TO CONFIDENTIALITY 
 
Between, the company P S.A.S with a capital of 3849045 €, 
Headquartered  at  1  rue  F.,  V.,  registered  in  the  MELUN  Trade  and  Companies  Register  under  number  000  000  000, 
represented by Mr. D. S., in his capacity as Chairman, 
hereinafter referred to as "P", 
On the one hand, 
 
And, the company _______________________ with a capital of _______________ €, 
Headquartered  at _______________________________,  registered with the  Registre  du Commerce et des Sociétés de 
_______________, under number _______________, represented by _______________, 
hereinafter referred to as "_______________", 
On the other hand, 
 
Hereinafter referred to jointly as the "Parties" or separately as a "Party". 
 
Whereas : 
The "Parties" will cooperate on joint projects within the scope of their respective normal activities, and will exchange 
technical and commercial information. 
The term "Confidential Information" includes, by way of non-limitative examples, databases, know-how, formulas, 
processes, drawings, sketches, photographs, plans, drafts, specifications, samples, reports, customer and supplier lists, 
pricing information, studies, results, inventions and ideas transmitted by one of the "Parties" to the other in connection 
with such projects.  
 
It has been agreed as follows: 
 
Each "Party" hereby acknowledges that any "Confidential Information" which may be made available to it by the 
other "Party", in any form whatsoever, is strictly confidential and may not be disclosed. 
 
The "Parties" therefore undertake, under the terms of this letter, to keep all such information confidential and, in 
particular, to : 
1. to use the "Confidential Information" only for the purposes of the project for which it was shared. The parties 
will refrain from using the "Confidential Information" that may be provided to them in any way that could be 
detrimental to the other "Party", i.e. its industrial and commercial activities, 
2. to limit by all appropriate means the total or partial distribution and use of the "Confidential Information" to 
employees and executives of their companies directly involved in the project. The "Parties" will take all 
necessary steps to ensure that their employees, managers and outside consultants keep the "Confidential 
Information" secret and confidential. 
3. the "Confidential Information" disclosed or made available by one of the "Parties" remains its property, to 
hand over to it, at its written request, any medium containing the "Confidential Information" disclosed or 
made available to it, or to destroy it.  
 
Each of the "Parties" acknowledges that the other "Party" would suffer certain and significant harm if it failed to 
comply with the confidentiality obligations contained in this letter.  
The "Parties" shall have no obligation with respect to any "Confidential Information" which is or may become public 
knowledge through no fault of their own. 
 
The "Parties" undertake to respect the commitments made in this letter for a period of 10 years (ten years) from the 
date of receipt of the "Confidential Information". 
 
To be effective, any amendment to this agreement must be in writing and signed by a duly authorized representative of 
the "Parties", their successor or assignee. 
This agreement is governed by French law and is subject to the exclusive jurisdiction of the Tribunal de Commerce de 
Melun. 
 
Signed in two original copies in Vaux-le-Pénil, on 21/03/2024 
 
For P,     For _______________, 
First name: D. S.    First name: _______________ 
Title : President     Title : _______________ 
Signature + stamp :    Signature + stamp : 
      


"""

    summary_witness = multiturn_generate_content_witness_statements(witness_message)

    nda_summary = multiturn_generate_content_witness_statements(nda)

    case_file = "cases.json"

    with open(case_file, 'r') as f:
        cases = load(f)


    # Now we need to compare the summaries with the cases in the file

    # 2 pass

    # pass 1 check if any relevance to our original case

    for case in cases.keys():
       information = cases[case]

       summary = multiturn_generate_content_pass_one(information, summary_witness+nda_summary)

       print(summary)

       break









    # extract_information('NDA 1.pdf')
    # multiturn_generate_content()