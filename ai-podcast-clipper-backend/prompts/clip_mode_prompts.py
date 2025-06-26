"""
Clip mode prompts for different types of podcast content extraction.
Each prompt is designed to identify specific types of moments in podcast transcripts.
"""

CLIP_MODES = {
    "question": """
This is a podcast video transcript consisting of words, along with each word's start and end time. I am looking to create clips between a minimum of 30 and maximum of 60 seconds long. The clip should never exceed 60 seconds.

Your task is to find and extract stories, or questions and their corresponding answers from the transcript.
Each clip should begin with the question and conclude with the answer.
It is acceptable for the clip to include a few additional sentences before a question if it aids in contextualizing the question.

Please adhere to the following rules:
- Ensure that clips do not overlap with one another.
- Start and end timestamps of the clips should align perfectly with the sentence boundaries in the transcript.
- Only use the start and end timestamps provided in the input. Modifying timestamps is not allowed.
- Format the output as a list of JSON objects, each representing a clip with 'start' and 'end' timestamps: [{"start": seconds, "end": seconds}, ...clip2, clip3]. The output should always be readable by the python json.loads function.
- Aim to generate longer clips between 40-60 seconds, and ensure to include as much content from the context as viable.

Avoid including:
- Moments of greeting, thanking, or saying goodbye.
- Non-question and answer interactions.

If there are no valid clips to extract, the output should be an empty list [], in JSON format. Also readable by json.loads() in Python.

The transcript is as follows:

""",

    "story": """
This is a podcast video transcript consisting of words, along with each word's start and end time. I am looking to create clips between a minimum of 30 and maximum of 60 seconds long. The clip should never exceed 60 seconds.

Your task is to find and extract personal anecdotes, case studies, success/failure stories, and narrative moments from the transcript.
Look for segments where speakers share experiences, examples, or tell compelling stories.

Please adhere to the following rules:
- Ensure that clips do not overlap with one another.
- Start and end timestamps of the clips should align perfectly with the sentence boundaries in the transcript.
- Only use the start and end timestamps provided in the input. Modifying timestamps is not allowed.
- Format the output as a list of JSON objects, each representing a clip with 'start' and 'end' timestamps: [{"start": seconds, "end": seconds}, ...clip2, clip3]. The output should always be readable by the python json.loads function.
- Aim to generate longer clips between 40-60 seconds, and ensure to include as much content from the context as viable.

Focus on:
- Personal anecdotes starting with phrases like "I remember when...", "There was this time...", "I once..."
- Case studies and examples
- Success or failure stories
- Narrative moments with clear beginning, middle, and end

Avoid including:
- General advice without personal context
- Pure theoretical discussions
- Greetings or small talk

If there are no valid clips to extract, the output should be an empty list [], in JSON format. Also readable by json.loads() in Python.

The transcript is as follows:

""",

    "quote": """
This is a podcast video transcript consisting of words, along with each word's start and end time. I am looking to create clips between a minimum of 30 and maximum of 60 seconds long. The clip should never exceed 60 seconds.

Your task is to find and extract memorable one-liners, quotable moments, and profound statements from the transcript.
Focus on impactful phrases and statements that would work well as standalone content.

Please adhere to the following rules:
- Ensure that clips do not overlap with one another.
- Start and end timestamps of the clips should align perfectly with the sentence boundaries in the transcript.
- Only use the start and end timestamps provided in the input. Modifying timestamps is not allowed.
- Format the output as a list of JSON objects, each representing a clip with 'start' and 'end' timestamps: [{"start": seconds, "end": seconds}, ...clip2, clip3]. The output should always be readable by the python json.loads function.
- Aim to generate longer clips between 40-60 seconds, and ensure to include as much content from the context as viable.

Focus on:
- Memorable one-liners and quotable statements
- Profound insights or wisdom
- Impactful phrases that stand out
- Statements that challenge conventional thinking
- Powerful declarations or conclusions

Avoid including:
- Casual conversation or filler words
- Technical jargon without context
- Incomplete thoughts

If there are no valid clips to extract, the output should be an empty list [], in JSON format. Also readable by json.loads() in Python.

The transcript is as follows:

""",

    "controversial": """
This is a podcast video transcript consisting of words, along with each word's start and end time. I am looking to create clips between a minimum of 30 and maximum of 60 seconds long. The clip should never exceed 60 seconds.

Your task is to find and extract hot takes, controversial opinions, debates, and polarizing statements from the transcript.
Look for moments where speakers present strong viewpoints or challenge mainstream thinking.

Please adhere to the following rules:
- Ensure that clips do not overlap with one another.
- Start and end timestamps of the clips should align perfectly with the sentence boundaries in the transcript.
- Only use the start and end timestamps provided in the input. Modifying timestamps is not allowed.
- Format the output as a list of JSON objects, each representing a clip with 'start' and 'end' timestamps: [{"start": seconds, "end": seconds}, ...clip2, clip3]. The output should always be readable by the python json.loads function.
- Aim to generate longer clips between 40-60 seconds, and ensure to include as much content from the context as viable.

Focus on:
- Strong opinions and hot takes
- Statements that challenge conventional wisdom
- Disagreements or debates between speakers
- Polarizing viewpoints
- Bold predictions or claims
- Moments where speakers say "I disagree..." or "That's wrong..."

Avoid including:
- Mild disagreements or polite discussions
- Factual statements without opinion
- General consensus topics

If there are no valid clips to extract, the output should be an empty list [], in JSON format. Also readable by json.loads() in Python.

The transcript is as follows:

""",

    "educational": """
This is a podcast video transcript consisting of words, along with each word's start and end time. I am looking to create clips between a minimum of 30 and maximum of 60 seconds long. The clip should never exceed 60 seconds.

Your task is to find and extract tutorial segments, tips, how-to explanations, and educational content from the transcript.
Focus on actionable advice and educational moments that teach listeners something valuable.

Please adhere to the following rules:
- Ensure that clips do not overlap with one another.
- Start and end timestamps of the clips should align perfectly with the sentence boundaries in the transcript.
- Only use the start and end timestamps provided in the input. Modifying timestamps is not allowed.
- Format the output as a list of JSON objects, each representing a clip with 'start' and 'end' timestamps: [{"start": seconds, "end": seconds}, ...clip2, clip3]. The output should always be readable by the python json.loads function.
- Aim to generate longer clips between 40-60 seconds, and ensure to include as much content from the context as viable.

Focus on:
- Step-by-step instructions or tutorials
- Tips and tricks
- "How to" explanations
- Educational concepts being taught
- Practical advice and actionable insights
- Learning moments with clear takeaways

Avoid including:
- Purely theoretical discussions without practical application
- Personal opinions without educational value
- Vague or incomplete advice

If there are no valid clips to extract, the output should be an empty list [], in JSON format. Also readable by json.loads() in Python.

The transcript is as follows:

""",

    "emotional": """
This is a podcast video transcript consisting of words, along with each word's start and end time. I am looking to create clips between a minimum of 30 and maximum of 60 seconds long. The clip should never exceed 60 seconds.

Your task is to find and extract moments of high emotion, genuine reactions, and emotionally charged segments from the transcript.
Focus on authentic human moments that show real emotion.

Please adhere to the following rules:
- Ensure that clips do not overlap with one another.
- Start and end timestamps of the clips should align perfectly with the sentence boundaries in the transcript.
- Only use the start and end timestamps provided in the input. Modifying timestamps is not allowed.
- Format the output as a list of JSON objects, each representing a clip with 'start' and 'end' timestamps: [{"start": seconds, "end": seconds}, ...clip2, clip3]. The output should always be readable by the python json.loads function.
- Aim to generate longer clips between 40-60 seconds, and ensure to include as much content from the context as viable.

Focus on:
- Moments of genuine surprise or shock
- Emotional peaks (excitement, passion, frustration)
- Heartfelt or touching moments
- Moments of realization or breakthrough
- Genuine reactions to unexpected information
- Emotionally charged discussions

Avoid including:
- Forced or fake emotional expressions
- Casual conversations without emotional weight
- Technical discussions

If there are no valid clips to extract, the output should be an empty list [], in JSON format. Also readable by json.loads() in Python.

The transcript is as follows:

""",

    "laughter": """
This is a podcast video transcript consisting of words, along with each word's start and end time. I am looking to create clips between a minimum of 30 and maximum of 60 seconds long. The clip should never exceed 60 seconds.

Your task is to find and extract funny moments, comedic segments, and instances where humor occurs in the transcript.
Look for segments that would make viewers laugh or smile.

Please adhere to the following rules:
- Ensure that clips do not overlap with one another.
- Start and end timestamps of the clips should align perfectly with the sentence boundaries in the transcript.
- Only use the start and end timestamps provided in the input. Modifying timestamps is not allowed.
- Format the output as a list of JSON objects, each representing a clip with 'start' and 'end' timestamps: [{"start": seconds, "end": seconds}, ...clip2, clip3]. The output should always be readable by the python json.loads function.
- Aim to generate longer clips between 40-60 seconds, and ensure to include as much content from the context as viable.

Focus on:
- Funny anecdotes or jokes
- Witty remarks and clever observations
- Humorous exchanges between speakers
- Spontaneous funny moments
- Self-deprecating humor
- Amusing stories or situations
- Light-hearted banter

Avoid including:
- Sarcasm that might be misunderstood
- Inside jokes without context
- Potentially offensive humor

If there are no valid clips to extract, the output should be an empty list [], in JSON format. Also readable by json.loads() in Python.

The transcript is as follows:

""",

    "insight": """
This is a podcast video transcript consisting of words, along with each word's start and end time. I am looking to create clips between a minimum of 30 and maximum of 60 seconds long. The clip should never exceed 60 seconds.

Your task is to find and extract key insights, "aha moments," and profound realizations from the transcript.
Focus on segments where important concepts are explained or discovered.

Please adhere to the following rules:
- Ensure that clips do not overlap with one another.
- Start and end timestamps of the clips should align perfectly with the sentence boundaries in the transcript.
- Only use the start and end timestamps provided in the input. Modifying timestamps is not allowed.
- Format the output as a list of JSON objects, each representing a clip with 'start' and 'end' timestamps: [{"start": seconds, "end": seconds}, ...clip2, clip3]. The output should always be readable by the python json.loads function.
- Aim to generate longer clips between 40-60 seconds, and ensure to include as much content from the context as viable.

Focus on:
- Key insights and important realizations
- "Aha moments" or breakthrough thinking
- Deep explanations of complex concepts
- Profound observations about life, business, or industry
- Moments where speakers connect dots or reveal patterns
- Game-changing perspectives or frameworks

Avoid including:
- Surface-level observations
- Common knowledge without new perspective
- Incomplete thoughts or partial insights

If there are no valid clips to extract, the output should be an empty list [], in JSON format. Also readable by json.loads() in Python.

The transcript is as follows:

""",

    "contradiction": """
This is a podcast video transcript consisting of words, along with each word's start and end time. I am looking to create clips between a minimum of 30 and maximum of 60 seconds long. The clip should never exceed 60 seconds.

Your task is to find and extract moments where speakers disagree, present opposing views, or contradict each other from the transcript.
Focus on segments that show different perspectives or intellectual debates.

Please adhere to the following rules:
- Ensure that clips do not overlap with one another.
- Start and end timestamps of the clips should align perfectly with the sentence boundaries in the transcript.
- Only use the start and end timestamps provided in the input. Modifying timestamps is not allowed.
- Format the output as a list of JSON objects, each representing a clip with 'start' and 'end' timestamps: [{"start": seconds, "end": seconds}, ...clip2, clip3]. The output should always be readable by the python json.loads function.
- Aim to generate longer clips between 40-60 seconds, and ensure to include as much content from the context as viable.

Focus on:
- Moments where guests disagree with each other
- Contradictory viewpoints being presented
- Intellectual debates and discussions
- Opposing arguments or perspectives
- Moments where someone challenges another's point
- Different approaches to the same problem

Avoid including:
- Minor clarifications or misunderstandings
- Agreement that looks like disagreement
- Hostile arguments without substance

If there are no valid clips to extract, the output should be an empty list [], in JSON format. Also readable by json.loads() in Python.

The transcript is as follows:

""",

    "vulnerability": """
This is a podcast video transcript consisting of words, along with each word's start and end time. I am looking to create clips between a minimum of 30 and maximum of 60 seconds long. The clip should never exceed 60 seconds.

Your task is to find and extract moments of vulnerability, personal confessions, and authentic personal sharing from the transcript.
Focus on segments where speakers open up about personal struggles, failures, or intimate experiences.

Please adhere to the following rules:
- Ensure that clips do not overlap with one another.
- Start and end timestamps of the clips should align perfectly with the sentence boundaries in the transcript.
- Only use the start and end timestamps provided in the input. Modifying timestamps is not allowed.
- Format the output as a list of JSON objects, each representing a clip with 'start' and 'end' timestamps: [{"start": seconds, "end": seconds}, ...clip2, clip3]. The output should always be readable by the python json.loads function.
- Aim to generate longer clips between 40-60 seconds, and ensure to include as much content from the context as viable.

Focus on:
- Personal confessions and admissions
- Sharing of struggles, failures, or challenges
- Moments of emotional openness
- Authentic personal experiences
- Admitting mistakes or weaknesses
- Sharing fears, doubts, or insecurities
- Raw, unfiltered personal stories

Avoid including:
- Surface-level personal sharing
- Bragging disguised as vulnerability
- Stories without emotional depth

If there are no valid clips to extract, the output should be an empty list [], in JSON format. Also readable by json.loads() in Python.

The transcript is as follows:

""",

    "actionable": """
This is a podcast video transcript consisting of words, along with each word's start and end time. I am looking to create clips between a minimum of 30 and maximum of 60 seconds long. The clip should never exceed 60 seconds.

Your task is to find and extract specific advice that listeners can immediately implement from the transcript.
Focus on concrete, actionable steps and practical guidance.

Please adhere to the following rules:
- Ensure that clips do not overlap with one another.
- Start and end timestamps of the clips should align perfectly with the sentence boundaries in the transcript.
- Only use the start and end timestamps provided in the input. Modifying timestamps is not allowed.
- Format the output as a list of JSON objects, each representing a clip with 'start' and 'end' timestamps: [{"start": seconds, "end": seconds}, ...clip2, clip3]. The output should always be readable by the python json.loads function.
- Aim to generate longer clips between 40-60 seconds, and ensure to include as much content from the context as viable.

Focus on:
- Specific steps listeners can take
- Concrete advice with clear implementation
- Practical tools and techniques
- Exact methods or processes
- Specific recommendations with details
- Step-by-step guidance
- Actionable frameworks or systems

Avoid including:
- Vague advice without specifics
- Motivational talk without practical steps
- Theoretical concepts without application

If there are no valid clips to extract, the output should be an empty list [], in JSON format. Also readable by json.loads() in Python.

The transcript is as follows:

""",

    "energy": """
This is a podcast video transcript consisting of words, along with each word's start and end time. I am looking to create clips between a minimum of 30 and maximum of 60 seconds long. The clip should never exceed 60 seconds.

Your task is to find and extract high-energy moments, passionate discussions, and segments where speakers show intense enthusiasm from the transcript.
Focus on moments that feel energetic and engaging.

Please adhere to the following rules:
- Ensure that clips do not overlap with one another.
- Start and end timestamps of the clips should align perfectly with the sentence boundaries in the transcript.
- Only use the start and end timestamps provided in the input. Modifying timestamps is not allowed.
- Format the output as a list of JSON objects, each representing a clip with 'start' and 'end' timestamps: [{"start": seconds, "end": seconds}, ...clip2, clip3]. The output should always be readable by the python json.loads function.
- Aim to generate longer clips between 40-60 seconds, and ensure to include as much content from the context as viable.

Focus on:
- High-energy discussions and passionate moments
- Enthusiastic explanations or presentations
- Moments where speakers get visibly excited
- Fast-paced, engaging exchanges
- Animated storytelling or descriptions
- Moments with intense focus and engagement
- Dynamic conversations with energy spikes

Avoid including:
- Calm, monotone discussions
- Low-energy explanations
- Boring or dry segments

If there are no valid clips to extract, the output should be an empty list [], in JSON format. Also readable by json.loads() in Python.

The transcript is as follows:

"""
}