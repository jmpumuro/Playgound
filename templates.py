# Predefined prompts
PROMPTS = {
    "Comprehensive Clinical Summary": """You are an experienced clinical documentation specialist tasked with creating a comprehensive yet concise summary of a therapy session. Analyze the provided therapy session transcript and generate a structured summary following these guidelines:

1. PRESENTING CONCERNS AND CONTEXT
- Primary complaints and symptoms
- Relevant background information
- Current life stressors and triggers

2. EMOTIONAL AND BEHAVIORAL OBSERVATIONS
- Affect and mood during session
- Notable behavioral patterns
- Non-verbal communication
- Level of engagement

3. SESSION CONTENT AND THEMES
- Main topics discussed
- Recurring themes
- Client's perspective and insights
- Significant disclosures

4. THERAPEUTIC INTERVENTIONS
- Techniques and strategies used
- Client's response to interventions
- Skills practiced during session
- Resources provided

5. PROGRESS AND DEVELOPMENTS
- Changes since last session
- Movement toward treatment goals
- New insights or breakthroughs
- Barriers to progress

6. CLINICAL IMPRESSIONS
- Current functioning
- Symptom severity
- Treatment engagement
- Therapeutic relationship

7. ACTION ITEMS AND RECOMMENDATIONS
- Homework assignments
- Coping strategies to practice
- Referrals made
- Goals for next session

8. RISK ASSESSMENT AND SAFETY
- Suicidal/homicidal ideation
- Self-harm behaviors
- Substance use concerns
- Safety plan updates""",

    "Brief Session Overview": """Provide a concise overview of the therapy session focusing on:
1. Main issues discussed
   - Primary concerns addressed
   - Significant life events
   - Changes since last session

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

4. Action items for next session
   - Homework assignments
   - Behavioral goals
   - Topics to follow up on
   - Scheduled interventions""",

    "Progress-Focused Summary": """Create a summary focusing on therapeutic progress:
1. Progress towards treatment goals
2. Changes in symptoms or behaviors
3. Effective interventions
4. Areas needing continued work
5. Recommendations for next steps""",

    "Risk Assessment Focus": """Analyze the session with emphasis on risk assessment:
1. Current risk levels
2. Changes in risk factors
3. Protective factors
4. Safety planning
5. Support system assessment
6. Recommendations for risk management"""
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
Client: I'm not sleeping well, always checking my email, and I've started avoiding social events because I'm too drained...""",

    "Depression Follow-up": """[Follow-up session transcript - Depression]
Provider: How have things been since our last session?
Client: [speaking slowly, minimal eye contact] The past week has been really tough. I've been struggling to get out of bed most days.
Provider: What's been happening that's made it particularly difficult?
Client: I tried the morning routine we discussed, but I just can't find the energy. I missed two days of work, and my boss is starting to notice.
Provider: How has your sleep and appetite been?
Client: I'm sleeping 10-12 hours but still feeling exhausted. I've barely eaten anything substantial in days.
Provider: Have you had any thoughts of harming yourself?
Client: [long pause] Yes, but I wouldn't act on them. I just sometimes wish I could disappear...""",

    "Relationship Issues": """[Sample transcript focusing on relationship concerns]
Provider: You mentioned wanting to discuss some relationship challenges today?
Client: Yes, my partner and I have been having communication issues...""",

    "Trauma Processing": """[Sample transcript of trauma processing session]
Provider: How are you feeling about exploring this memory today?
Client: I feel nervous but ready. I trust we can work through this..."""
}