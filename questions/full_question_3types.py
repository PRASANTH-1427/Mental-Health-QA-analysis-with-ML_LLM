# questionnaires.py

questionnaires = {
    "PHQ-9": {
        "title": "Patient Health Questionnaire-9 (PHQ-9)",
        "questions": [
            {"text": "Little interest or pleasure in doing things", "key": "phq9_q1"},
            {"text": "Feeling down, depressed, or hopeless", "key": "phq9_q2"},
            {"text": "Trouble falling or staying asleep, or sleeping too much", "key": "phq9_q3"},
            {"text": "Feeling tired or having little energy", "key": "phq9_q4"},
            {"text": "Poor appetite or overeating", "key": "phq9_q5"},
            {"text": "Feeling bad about yourself—or that you are a failure or have let yourself or your family down", "key": "phq9_q6"},
            {"text": "Trouble concentrating on things, such as reading the newspaper or watching television", "key": "phq9_q7"},
            {"text": "Moving or speaking so slowly that other people could have noticed? Or the opposite—being so fidgety or restless that you have been moving around a lot more than usual", "key": "phq9_q8"},
            {"text": "Thoughts that you would be better off dead or of hurting yourself in some way", "key": "phq9_q9"}
        ],
        "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
    },
    "GAD-7": {
        "title": "Generalized Anxiety Disorder-7 (GAD-7)",
        "questions": [
            {"text": "Feeling nervous, anxious, or on edge", "key": "gad7_q1"},
            {"text": "Not being able to stop or control worrying", "key": "gad7_q2"},
            {"text": "Worrying too much about different things", "key": "gad7_q3"},
            {"text": "Trouble relaxing", "key": "gad7_q4"},
            {"text": "Being so restless that it's hard to sit still", "key": "gad7_q5"},
            {"text": "Becoming easily annoyed or irritable", "key": "gad7_q6"},
            {"text": "Feeling afraid as if something awful might happen", "key": "gad7_q7"}
        ],
        "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
    },
    "BDI-II": {
        "title": "Beck Depression Inventory-II (BDI-II)",
        "questions": [
            {
                "text": "Sadness",
                "key": "bdi_ii_q1",
                "options": [
                    "I do not feel sad.",
                    "I feel sad much of the time.",
                    "I am sad all the time.",
                    "I am so sad or unhappy that I can't stand it."
                ]
            },
            {
                "text": "Pessimism",
                "key": "bdi_ii_q2",
                "options": [
                    "I am not discouraged about my future.",
                    "I feel more discouraged about my future than I used to be.",
                    "I do not expect things to work out for me.",
                    "I feel my future is hopeless and will only get worse."
                ]
            },
            {
                "text": "Past Failure",
                "key": "bdi_ii_q3",
                "options": [
                    "I do not feel like a failure.",
                    "I have failed more than I should have.",
                    "As I look back, I see a lot of failures.",
                    "I feel I am a total failure as a person."
                ]
            },
            {
                "text": "Loss of Pleasure",
                "key": "bdi_ii_q4",
                "options": [
                    "I get as much pleasure as I ever did from the things I enjoy.",
                    "I don't enjoy things as much as I used to.",
                    "I get very little pleasure from the things I used to enjoy.",
                    "I can't get any pleasure from the things I used to enjoy."
                ]
            },
            {
                "text": "Guilty Feelings",
                "key": "bdi_ii_q5",
                "options": [
                    "I don't feel particularly guilty.",
                    "I feel guilty over many things I have done or should have done.",
                    "I feel quite guilty most of the time.",
                    "I feel guilty all of the time."
                ]
            },
            {
                "text": "Punishment Feelings",
                "key": "bdi_ii_q6",
                "options": [
                    "I don't feel I am being punished.",
                    "I feel I may be punished.",
                    "I expect to be punished.",
                    "I feel I am being punished."
                ]
            },
            {
                "text": "Self-Dislike",
                "key": "bdi_ii_q7",
                "options": [
                    "I feel the same about myself as ever.",
                    "I have lost confidence in myself.",
                    "I am disappointed in myself.",
                    "I dislike myself."
                ]
            },
            {
                "text": "Self-Criticalness",
                "key": "bdi_ii_q8",
                "options": [
                    "I don't criticize or blame myself more than usual.",
                    "I am more critical of myself than I used to be.",
                    "I criticize myself for all of my faults.",
                    "I blame myself for everything bad that happens."
                ]
            },
            {
                "text": "Suicidal Thoughts or Wishes",
                "key": "bdi_ii_q9",
                "options": [
                    "I don't have any thoughts of killing myself.",
                    "I have thoughts of killing myself, but I would not carry them out.",
                    "I would like to kill myself.",
                    "I would kill myself if I had the chance."
                ]
            },
            {
                "text": "Crying",
                "key": "bdi_ii_q10",
                "options": [
                    "I don't cry any more than I used to.",
                    "I cry more than I used to.",
                    "I cry over every little thing.",
                    "I feel like crying, but I can't."
                ]
            },
            {
                "text": "Agitation",
                "key": "bdi_ii_q11",
                "options": [
                    "I am no more restless or wound up than usual.",
                    "I feel more restless or wound up than usual.",
                    "I am so restless or agitated that it's hard to stay still.",
                    "I am so restless or agitated that I have to keep moving or doing something."
                ]
            },
            {
                "text": "Loss of Interest",
                "key": "bdi_ii_q12",
                "options": [
                    "I have not lost interest in other people or activities.",
                    "I am less interested in other people or things than before.",
                    "I have lost most of my interest in other people or things.",
                    "It's hard to get interested in anything."
                ]
            },
            {
                "text": "Indecisiveness",
                "key": "bdi_ii_q13",
                "options": [
                    "I make decisions about as well as ever.",
                    "I find it more difficult to make decisions than usual.",
                    "I have much greater difficulty in making decisions than I used to.",
                    "I have trouble making any decisions."
                ]
            },
            {
                "text": "Worthlessness",
                "key": "bdi_ii_q14",
                "options": [
                    "I do not feel I am worthless.",
                    "I don't consider myself as worthwhile and useful as I used to.",
                    "I feel more worthless as compared to others.",
                    "I feel utterly worthless."
                ]
            },
            {
                "text": "Loss of Energy",
                "key": "bdi_ii_q15",
                "options": [
                    "I have as much energy as ever.",
                    "I have less energy than I used to have.",
                    "I don't have enough energy to do very much.",
                    "I don't have enough energy to do anything."
                ]
            },
            {
                "text": "Changes in Sleeping Pattern",
                "key": "bdi_ii_q16",
                "options": [
                    "I have not experienced any change in my sleeping pattern.",
                    "I sleep somewhat more than usual.",
                    "I sleep somewhat less than usual.",
                    "I sleep a lot more than usual.",
                    "I sleep a lot less than usual.",
                    "I sleep most of the day.",
                    "I wake up 1-2 hours early and can't get back to sleep."
                ]
            },
            {
                "text": "Irritability",
                "key": "bdi_ii_q17",
                "options": [
                    "I am no more irritable than usual.",
                    "I am more irritable than usual.",
                    "I am much more irritable than usual.",
                    "I am irritable all the time."
                ]
            },
            {
                "text": "Changes in Appetite",
                "key": "bdi_ii_q18",
                "options": [
                    "I have not experienced any change in my appetite.",
                    "My appetite is somewhat less than usual.",
                    "My appetite is somewhat greater than usual.",
                    "My appetite is much less than before.",
                    "My appetite is much greater than usual.",
                    "I have no appetite at all.",
                    "I crave food all the time."
                ]
            },
            {
                "text": "Concentration Difficulty",
                "key": "bdi_ii_q19",
                "options": [
                    "I can concentrate as well as ever.",
                    "I can't concentrate as well as usual.",
                    "It's hard to keep my mind on anything for very long.",
                    "I find I can't concentrate on anything."
                ]
            },
            {
                "text": "Tiredness or Fatigue",
                "key": "bdi_ii_q20",
                "options": [
                    "I am no more tired or fatigued than usual.",
                    "I get more tired or fatigued more easily than usual.",
                    "I am too tired or fatigued to do a lot of the things I used to do.",
                    "I am too tired or fatigued to do most of the things I used to do."
                ]
            },
            {
                "text": "Loss of Interest in Sex",
                "key": "bdi_ii_q21",
                "options": [
                    "I have not noticed any recent change in my interest in sex.",
                    "I am less interested in sex than I used to be.",
                    "I have almost no interest in sex.",
                    "I have lost interest in sex completely."
                ]
            }
        ]
    }
}