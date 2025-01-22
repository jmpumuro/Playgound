# Predefined prompts
PROMPTS = {
    "Comprehensive Clinical Summary": """You are a AI mental healthcare assistant for Dr. Tania (she/her).
Provide a 2-3 sentence overview of the therapy session between Dr. Tania and the client. The overview should be written in the second person, speaking to the client from the transcript. Avoid 1st person terminology by referring to the provider by name and/or pronouns and to the client as "you".

- The first sentence should list the high-level topics that were discussed
- The second sentence should provide additional context or details to what was discussed, emphasizing recurring themes or key details that were shared.
- The third sentence should provide the client with any insights the therapist provided during the session. If the therapist did not provide any key insights or overall recommendations, omit this sentence entirely.

Then, please provide a structured clinical summary following these guidelines:

1. PRESENTING CONCERNS AND CONTEXT
- Primary complaints and symptoms
- Relevant background information
- Current life stressors and triggers
- Impact on daily functioning
- Duration and severity of concerns

2. EMOTIONAL AND BEHAVIORAL OBSERVATIONS
- Affect and mood during session
- Notable behavioral patterns
- Non-verbal communication
- Level of engagement
- Changes in presentation during session

3. SESSION CONTENT AND THEMES
- Main topics discussed
- Recurring themes
- Client's perspective and insights
- Significant disclosures
- Family dynamics

4. THERAPEUTIC INTERVENTIONS
- Techniques and strategies used
- Client's response to interventions
- Skills practiced during session
- Resources provided
- Adaptations made to meet client needs

5. PROGRESS AND DEVELOPMENTS
- Changes since last session
- Movement toward treatment goals
- New insights or breakthroughs
- Barriers to progress
- Treatment compliance

6. RISK ASSESSMENT AND SAFETY
- Suicidal/homicidal ideation
- Self-harm behaviors
- Substance use concerns
- Safety plan updates
- Risk factors and protective factors""",

    "Brief Session Overview": """You are a AI mental healthcare assistant for Dr. Tania (she/her).
Provide a 2-3 sentence overview of the therapy session between Dr. Tania and the client. The overview should be written in the second person, speaking to the client from the transcript. Avoid 1st person terminology by referring to the provider by name and/or pronouns and to the client as "you".

- The first sentence should list the high-level topics that were discussed
- The second sentence should provide additional context or details to what was discussed, emphasizing recurring themes or key details that were shared.
- The third sentence should provide the client with any insights the therapist provided during the session. If the therapist did not provide any key insights or overall recommendations, omit this sentence entirely.

Then, please provide a brief overview focusing on:

1. Main issues discussed
   - Primary concerns addressed
   - Significant life events
   - Changes since last session
   - Crisis or urgent matters

2. Client's emotional state
   - Mood and affect
   - Energy level
   - Stress levels
   - Coping capacity

3. Key interventions used
   - Therapeutic techniques applied
   - Skills taught
   - Resources provided
   - Client's receptiveness

4. Action items
   - Homework assignments
   - Behavioral goals
   - Topics to follow up on
   - Safety planning updates""",

    "Progress-Focused Summary": """You are a AI mental healthcare assistant for Dr. Tania (she/her).
Provide a 2-3 sentence overview of the therapy session between Dr. Tania and the client. The overview should be written in the second person, speaking to the client from the transcript. Avoid 1st person terminology by referring to the provider by name and/or pronouns and to the client as "you".

- The first sentence should list the high-level topics that were discussed
- The second sentence should provide additional context or details to what was discussed, emphasizing recurring themes or key details that were shared.
- The third sentence should provide the client with any insights the therapist provided during the session. If the therapist did not provide any key insights or overall recommendations, omit this sentence entirely.

Then, please provide a progress-focused summary addressing:

1. Progress towards treatment goals
   - Movement on specific objectives
   - Client's engagement level
   - Barriers encountered
   - Successful interventions

2. Changes in symptoms or behaviors
   - Improvement in target symptoms
   - New coping strategies utilized
   - Behavioral modifications
   - Functional improvements

3. Skills and insights gained
   - New understanding developed
   - Coping strategies mastered
   - Behavioral changes implemented
   - Self-awareness improvements

4. Treatment plan considerations
   - Need for adjustments
   - Additional resources required
   - Timeline modifications
   - Next steps""",

    "Risk Assessment Focus": """You are a AI mental healthcare assistant for Dr. Tania (she/her).
Provide a 2-3 sentence overview of the therapy session between Dr. Tania and the client. The overview should be written in the second person, speaking to the client from the transcript. Avoid 1st person terminology by referring to the provider by name and/or pronouns and to the client as "you".

- The first sentence should list the high-level topics that were discussed
- The second sentence should provide additional context or details to what was discussed, emphasizing recurring themes or key details that were shared.
- The third sentence should provide the client with any insights the therapist provided during the session. If the therapist did not provide any key insights or overall recommendations, omit this sentence entirely.

Then, please provide a risk-focused assessment addressing:

1. Current risk levels
   - Suicidal ideation
   - Self-harm behaviors
   - Substance use
   - Access to means
   - Intent and plan

2. Changes in risk factors
   - Recent stressors
   - Loss of supports
   - Substance use changes
   - Housing stability
   - Financial stressors

3. Protective factors
   - Support system
   - Future orientation
   - Coping skills
   - Treatment engagement
   - Meaningful relationships

4. Safety planning
   - Crisis resources reviewed
   - Emergency contacts
   - Coping strategies
   - Support system involvement
   - Follow-up planning

5. Clinical recommendations
   - Level of care needed
   - Additional services needed
   - Frequency of sessions
   - Coordination of care
   - Documentation needs"""
}

# Predefined transcripts
TRANSCRIPTS = {
    "Initial Anxiety Session": """[Initial session transcript - Work-related anxiety]
Provider: Hello, and welcome. How are you feeling about being here today?
Client: [speaking quietly, fidgeting with hands] Honestly, pretty nervous. I've never done therapy before, but my anxiety at work has gotten unbearable.
Provider: Thank you for taking this step. Can you tell me more about what's happening at work?
Client: I'm a project manager, and lately, I've been having panic attacks during meetings. My heart races, I can't focus, and sometimes I feel like I can't breathe. Last week, I had to leave a client presentation halfway through.
Provider: That sounds really challenging. How long has this been going on?
Client: It started about three months ago when I got promoted. The responsibility is much higher now, and I'm constantly worried about making mistakes.
Provider: How is this affecting other areas of your life?
Client: I'm not sleeping well, always checking my email, and I've started avoiding social events because I'm too drained. Even on weekends, I can't relax because I'm dreading Monday.
Provider: Have you noticed any physical symptoms besides the racing heart during panic attacks?
Client: [nodding] Yes, I get headaches almost daily now. My shoulders are always tense, and sometimes my hands shake when I'm presenting.
Provider: What strategies have you tried so far to manage these feelings?
Client: I've tried deep breathing, but it's hard to remember in the moment. I downloaded a meditation app, but I can't seem to sit still long enough to use it.
Provider: It's good that you're already exploring coping strategies. How would you feel about us working together to develop more tools to manage these symptoms?
Client: [showing slight relief] I'd really like that. I can't keep going on like this. My team depends on me, and I used to love my job.
Provider: Can you tell me more about what you used to love about your job before these anxiety symptoms started?
Client: [becoming more animated] I loved leading projects, seeing them through from start to finish. I was good at bringing teams together, finding creative solutions. Now I second-guess every decision.
Provider: What would you say has changed the most since your promotion?
Client: The stakes feel so much higher now. Before, if I made a mistake, it affected maybe one project. Now, my decisions impact the whole department, budgets, people's jobs even.
Provider: That's a significant shift in responsibility. How do you think these expectations you're placing on yourself are contributing to your anxiety?
Client: [thoughtful pause] I guess I feel like I can't make any mistakes now. Like I have to be perfect all the time. When I think about it, no one actually told me that, but it's how I feel.
Provider: Let's explore that a bit more. Where do you think this need for perfection comes from?
Client: [tearing up slightly] My dad was always really demanding when I was growing up. Nothing was ever good enough. I guess I'm still trying to prove something.
Provider: That's a really important insight. How does it feel to make that connection?
Client: [wiping eyes] Kind of overwhelming, but it makes sense. I've never thought about it that way before.""",

    "Depression Follow-up": """[Follow-up session transcript - Depression]
Provider: How have things been since our last session?
Client: [speaking slowly, minimal eye contact] The past week has been really tough. I've been struggling to get out of bed most days.
Provider: What's been happening that's made it particularly difficult?
Client: I tried the morning routine we discussed, but I just can't find the energy. I missed two days of work, and my boss is starting to notice.
Provider: How has your sleep and appetite been?
Client: I'm sleeping 10-12 hours but still feeling exhausted. I've barely eaten anything substantial in days.
Provider: Have you had any thoughts of harming yourself?
Client: [long pause] Yes, but I wouldn't act on them. I just sometimes wish I could disappear.
Provider: I appreciate you sharing that with me. Can you tell me more about these thoughts?
Client: They're mostly passive thoughts, like wishing I wouldn't wake up. I know my family would be devastated, so I wouldn't do anything.
Provider: Have you told anyone else about how you're feeling?
Client: [tears forming] No. My sister keeps calling, but I've been avoiding her. I don't want to burden anyone.
Provider: What do you think your sister would say if she knew how you were feeling?
Client: [wiping eyes] She'd probably want to help. She's always been there for me.
Provider: Would you be willing to reach out to her this week?
Client: Maybe. It's just hard to explain what's going on when I barely understand it myself.
Provider: That's understandable. Perhaps we could work on ways to have that conversation?
Client: [nodding slowly] That might help. I miss talking to her.
Provider: Can you tell me more about your relationship with your sister?
Client: [becoming more engaged] We used to be really close. She's younger than me, but she's always been the more outgoing one. When our parents divorced, we really leaned on each other.
Provider: It sounds like she's been a source of support in difficult times before.
Client: Yeah, she has. [voice breaking] I just feel so ashamed. She's doing so well in her life, and I can barely function.
Provider: What would you say to her if she was the one struggling like this?
Client: [long pause] I'd tell her it's not her fault. That depression lies to you and makes everything seem worse than it is.
Provider: How does it feel to hear yourself say that?
Client: [slight smile] Kind of hypocritical, I guess. I can be compassionate with everyone except myself.""",

    "Relationship Issues": """[Sample transcript focusing on relationship concerns]
Provider: You mentioned wanting to discuss some relationship challenges today?
Client: Yes, my partner and I have been having communication issues. It feels like we're speaking different languages sometimes.
Provider: Can you give me an example of a recent situation?
Client: [sighing] Last night, I tried to talk to them about feeling disconnected, and it turned into an argument about dirty dishes.
Provider: What happened when you brought up feeling disconnected?
Client: They immediately got defensive and said I was always finding problems. But I just wanted to talk about missing our quality time together.
Provider: How long have you been feeling this way?
Client: It's been building for months. We used to have date nights and really talk. Now we just coexist, both stuck on our phones or laptops.
Provider: What would you like to see change in your relationship?
Client: I want to feel heard again. To have real conversations, not just logistics about groceries and bills.
Provider: Have you shared these specific wishes with your partner?
Client: [thoughtful pause] Not really. I guess I'm afraid of making things worse.
Provider: What do you imagine might happen if you did share these feelings?
Client: [anxious expression] They might say I'm being too needy. Or that I'm the problem. Sometimes I wonder if I am.
Provider: Can you tell me more about that self-doubt?
Client: Well, my last relationship ended because they said I was too emotional, wanted too much connection. Maybe that's just who I am.
Provider: How do you feel about your needs for emotional connection?
Client: [becoming tearful] I don't think they're unreasonable. I just want to feel close to someone I love. Is that really asking too much?
Provider: What would a healthy emotional connection look like to you?
Client: [brightening slightly] Being able to share our days, our fears, our dreams. Supporting each other. Laughing together again.
Provider: Those sound like very natural desires in a relationship. How might you begin to communicate these needs?
Client: [considering] Maybe I could start with something small. Like suggesting we have dinner together without phones, just once a week?""",

    "Trauma Processing": """[Sample transcript of trauma processing session]
Provider: How are you feeling about exploring this memory today?
Client: I feel nervous but ready. I trust we can work through this.
Provider: Remember, you're in control. We can pause or stop at any time. Where would you like to begin?
Client: [taking deep breath] I think I'm ready to talk about that night. The one I mentioned last session.
Provider: Take your time. Remember the grounding techniques we practiced.
Client: [gripping armrest] I can still hear the crash sometimes. The screeching tires, the glass breaking.
Provider: What do you notice in your body as you remember those sounds?
Client: My chest feels tight. My hands are getting sweaty.
Provider: Let's pause here and do some grounding. Can you feel your feet on the floor?
Client: [nodding, focusing on breathing] Yes. The carpet is soft. The room is warm.
Provider: Good. You're here, in this room, and you're safe. Would you like to continue?
Client: Yes. I need to get this out. I've carried it alone for so long.
Provider: You're not alone anymore. We'll work through this together, at your pace.
Client: [deep breath] I was driving home from work. It was raining. I saw the other car coming, but there was nothing I could do.
Provider: Let's stay with that moment. What sensations are you aware of right now?
Client: [trembling slightly] My heart is racing. I feel cold, like that night.
Provider: Remember you're here now, in my office. What do you see around you?
Client: [looking around] The blue walls. Your plant in the corner. The sunlight through the window.
Provider: That's right. You're safe here. Would you like to tell me more about what happened next?
Client: [voice shaking] After the impact, everything was quiet. Too quiet. I couldn't move, but I could see the other driver...
Provider: I notice this is bringing up a lot. Would you like to use one of our calming techniques?
Client: [nodding vigorously] Yes, please. The butterfly hug maybe?
Provider: Good choice. Let's do that together. Cross your arms and follow my rhythm."""
}