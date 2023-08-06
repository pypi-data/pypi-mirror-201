from datetime import datetime, timedelta
import json
from stackapi import StackAPI, StackAPIError


def get_qa(site: str, tag: str|None=None, text: str|None=None, days: int=365, num: int=1000, out: str|None=None) -> None:
    site = StackAPI(site, version='2.3')
    site.page_size = 100
    site.max_pages = ((num - 1) // 100) + 1
    try:
        start = fromdate=datetime.now() - timedelta(days=days)
        if tag and text:
            result = site.fetch('search/advanced', title=text, tagged=tag, fromdate=start, accepted=True)
        elif tag:
            result = site.fetch('search/advanced', tagged=tag, fromdate=start, accepted=True)
        elif text:
            result = site.fetch('search/advanced', title=text, fromdate=start, accepted=True)
        else:
            result = site.fetch('search/advanced', fromdate=start, accepted=True)
        question_ids = []
        answer_ids = []
        for item in result['items']:
            question_ids.append(item['question_id'])
            answer_ids.append(item['accepted_answer_id'])

        # Now get the details
        titles = []
        questions = []
        answers = []
        scores = []
        #upvotes = []
        #downvotes = []

        while question_ids:
            # I created the filter using the page https://api.stackexchange.com/docs/questions-by-ids
            # It includes title, body, score, and upvotes.
            # According to docs, filters are immutable and non-expiring
            result = site.fetch('questions', ids=question_ids[:100], 
                                filter='!DE-5b3_dCjF*D6Q8gxC3*7E7KAAFO4NUqVe1b4)OCxGPj3EQ2DX')
            question_ids = question_ids[100:]
            for item in result['items']:
                titles.append(item['title'])
                questions.append(item['body_markdown'])
                scores.append(item['score'])
                #downvotes.append(item['down_vote_count'])
                #upvotes.append(item['up_vote_count'])
                
        while answer_ids:
            result = site.fetch('answers', ids=answer_ids[:100], filter='!)Q0*LNlnf79TzVMQwRAWZx-n')
            answer_ids = answer_ids[100:]
            for item in result['items']:
                answers.append(item['body_markdown'])

        results = []
        for item in zip(titles, questions, answers, scores) #, upvotes, downvotes):
            results.append({
                'title': item[0],
                'question': item[1],
                'answer': item[2],
                'score': item[3],
                #'upvotes': item[4],
                #'downvotes': item[5],
            })
        if out:
            with open(out, 'w') as f:
                json.dump(results, f)
        else:
            print(json.dumps(results))

    except StackAPIError as e:
        print("   Error URL: {}".format(e.url))
        print("   Error Code: {}".format(e.code))
        print("   Error Error: {}".format(e.error))
        print("   Error Message: {}".format(e.message))


