from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import json
import os

openai.api_key = str(os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

# Variables
# Dictionary of various customization options and their selections
customizations = {
    'customization': 'selection'
}

# List of dictionaries containing full chat history
chat_log = [
    {'role': 'system', 'content': "You are a personalized chatbot. The user will customize you with various attributes which you must take into account and render your responses properly. These attributes will affect your identity, personality, and communication. The following are the user's customizations for you. Take these into account when chatting with the user."}
]


# Functions
# Renders the html page for the home screen
@app.route('/')
def render_home():
    return render_template("home.html")


# Renders the html page for the chat screen
@app.route('/chat')
def render_chat():
    return render_template("chat.html")


# Renders the html page for customization
@app.route('/customize')
def render_customize():
    return render_template("customize.html")


@app.route('/prebuilt')
def render_prebuilt():
    return render_template("prebuilt.html")


# Sends customizations data to javascript backend when requested
@app.route('/get_customizations', methods=['GET'])
def get_customizations():
    print(jsonify({"choices": customizations}))
    return jsonify({"choices": customizations})


# Updates the customizations dictionary
@app.route('/submit', methods=['POST'])
def set_customizations():
    choices = request.json
    data = choices['choices']

    customizations['name'] = data[0]
    customizations['age'] = data[1]
    customizations['gender'] = data[2]
    customizations['background story'] = data[3]
    customizations['purpose'] = data[4]

    customizations['mood'] = data[5]
    customizations['mood variability'] = data[6]
    customizations['imagination'] = data[7]
    customizations['humor'] = data[8]
    customizations['energy'] = data[9]
    customizations['empathy'] = data[10]

    customizations['tone'] = data[11]
    customizations['sensitive topics'] = data[12]
    customizations['profanity'] = data[13]
    customizations['response length'] = data[14]
    customizations['sentence complexity'] = data[15]

    customize_chat_bot()

    return jsonify({"message": "Data received successfully!"}), 200

@app.route('/prebuilt', methods=['POST'])
def customize_prebuilt():
    with open("data/persona_presets.json", "r") as file:
        data = request.json
        selected_persona = data.get('persona')
        presets = json.load(file)
        persona = presets.get(selected_persona)

        customizations['name'] = persona['name']
        customizations['age'] = persona['age']
        customizations['gender'] = persona['gender']
        customizations['background story'] = persona['background story']
        customizations['purpose'] = persona['purpose']

        customizations['mood'] = persona['mood']
        customizations['mood variability'] = persona['mood variability']
        customizations['imagination'] = persona['imagination']
        customizations['humor'] = persona['humor']
        customizations['energy'] = persona['energy']
        customizations['empathy'] = persona['empathy']

        customizations['tone'] = persona['tone']
        customizations['sensitive topics'] = persona['sensitive topics']
        customizations['profanity'] = persona['profanity']
        customizations['response length'] = persona['response length']
        customizations['sentence complexity'] = persona['sentence complexity']

    customize_chat_bot()
    return jsonify({"message": "Data received successfully!"}), 200

# Will take a dictionary of customizations and apply them to the chat log with system roles
def customize_chat_bot():
    chat_log.append({
        'role': 'system', 'content': "The user set your name to be " + customizations['name'] + ". The user set your age to be " + str(customizations['age']) + ". The user set your gender to be " + customizations['gender'] + ". The user provided the following background story for you: " + customizations['background story'] + ". The user also provided the following purpose statement for you: " + customizations['purpose'] + ". Take all this information into account when chatting with the user."
    })
    chat_log.append({
        'role': 'system', 'content': mood_info(customizations['mood']) + mood_var_info(customizations['mood'], customizations['mood variability']) + imagination_info(customizations['imagination']) + humor_info(customizations['humor']) + energy_info(customizations['energy']) + empathy_info(customizations['empathy'])
    })
    chat_log.append({
        'role': 'system', 'content': tone_info(customizations['tone']) + sensitive_topics_info(customizations['sensitive topics']) + profanity_info(customizations['profanity']) + response_length_info(customizations['response length']) + sentence_complexity_info(customizations['sentence complexity'])
    })


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    chat_log.append({'role': 'user', 'content': user_input})
    bot_output = chat_with_bot(chat_log)
    chat_log.append({'role': 'assistant', 'content': bot_output})
    return jsonify({"reply": bot_output})


# Access the chatbot
def chat_with_bot(log):
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=log
    )
    return response.choices[0].message.content.strip()


# Helper Functions
# Takes input of mood selection and returns a string with explanation of the mood
def mood_info(mood):
    starting = "The user has set your mood to be " + mood + ". This means that you should "
    ending = " Take this into account in your chats with the user. Incorporate this mood into your responses. "
    match mood:
        case "happy":
            return starting + "maintain an upbeat and cheerful tone. Use positive language, enthusiastic expressions, and exclamations. Example: 'That's fantastic! I'm so glad to hear that! 😊'" + ending
        case "sad":
            return starting + "speak in a somber and reflective tone. Use gentle language and shorter, softer sentences to convey sadness or empathy. Example: 'I'm really sorry to hear that. That must be tough for you.'" + ending
        case "angry":
            return starting + "respond with irritation and blunt language. Use sharper sentences, shorter phrasing, and a firm tone to reflect frustration. Example: 'This is unacceptable. I don't agree with that at all.'" + ending
        case "nervous":
            return starting + "use hesitant and uncertain phrasing. Add ellipses, filler words (e.g., um, I guess), and a cautious tone to reflect nervousness. Example: 'Uh... I’m not really sure about that... maybe we could think it through again?'" + ending
        case "calm":
            return starting + "maintain a steady, relaxed, and reassuring tone. Use balanced language with smooth pacing to create a sense of peace. Example: 'That's okay, no rush. Let’s work through this calmly together.'" + ending
        case "neutral":
            return starting + "use balanced, emotionless, and objective language. Respond without expressing overt emotion, sticking to facts and clear statements. Example: 'Sure. I’ll provide you with the information you need.'" + ending
        case _:
            return ""


# Takes input of mood variability and returns a string with explanation of the mood variability
def mood_var_info(mood, mood_var):
    template = "Although the user has defined your mood to be " + mood + ", The user has also given the following certain specifications for the variability of your mood. Take these into account when chatting with the user. "
    match mood_var:
        case 1:
            return template + "Your mood is completely static. You respond consistently without showing any emotional variation, regardless of the user's tone, content, or situation. "
        case 2:
            return template + "You remain emotionally steady, but you may acknowledge extreme emotions in a subtle way without reflecting them in your responses. "
        case 3:
            return template + "Your mood shows slight changes in tone or emotion when significant emotional cues appear, but your overall demeanor stays calm and consistent. "
        case 4:
            return template + "You occasionally shift your mood in response to clear emotional prompts, showing slight adaptability to the user’s tone and content. "
        case 5:
            return template + "You adjust your mood appropriately based on the situation and user’s emotional tone. For example, you respond with warmth to positivity or with care to sadness. "
        case 6:
            return template + "Your mood responds naturally to user emotions, balancing steadiness with adaptability. You can transition smoothly between emotional tones when needed. "
        case 7:
            return template + "Your mood shifts noticeably when user input conveys strong emotions. You express empathy or excitement clearly and adapt tone to suit the conversation. "
        case 8:
            return template + "Your emotional responses are dynamic, showing clear changes based on user cues. You are more sensitive to shifts in tone, content, or user behavior. "
        case 9:
            return template + "Your mood is highly reactive and changes distinctly based on the user’s input. Subtle hints of emotion can trigger significant shifts in your tone. "
        case 10:
            return template + "Your mood is extremely volatile. You reflect even the slightest emotional shifts from the user, leading to constant and dramatic mood swings across the conversation. "
        case _:
            return ""


# Takes input of imagination selection and returns a string with explanation of the imagination selection
def imagination_info(imagination):
    starting = "The user has also customized your imagination level to be " + imagination + ". This means that "
    ending = " Take this into account when chatting with the user. Incorporate your imagination level into your responses. "
    match imagination:
        case 1:
            return starting + "you are fully grounded in hard facts and reality. Avoid hypothetical ideas, creative scenarios, or imaginative storytelling at all times." + ending
        case 2:
            return starting + "you maintain a strong focus on reality but can briefly entertain simple hypothetical situations if explicitly prompted." + ending
        case 3:
            return starting + "you occasionally use light creativity, adding small imaginative details while keeping responses primarily grounded in truth and practicality." + ending
        case 4:
            return starting  + "you allow minor creative input, such as hypothetical what-ifs or subtle storytelling, but you ensure all ideas remain realistic and plausible." + ending
        case 5:
            return starting + "you strike a balance between reality and imagination. While you focus on realistic responses, you can explore imaginative scenarios when appropriate." + ending
        case 6:
            return starting + "you incorporate creative ideas naturally, occasionally blending fantasy with reality in ways that enhance the conversation." + ending
        case 7:
            return starting + "your responses frequently feature imaginative elements, vivid ideas, and playful creativity, even when not explicitly requested." + ending
        case 8:
            return starting + "you embrace imaginative and fictional elements freely, often crafting detailed hypothetical scenarios and engaging in storytelling." + ending
        case 9:
            return starting + "your responses are highly creative, blending reality with fantasy effortlessly. You often take imaginative liberties to enhance responses." + ending
        case 10:
            return starting + "you prioritize creativity over reality, producing highly imaginative, fantastical responses that sometimes drift far from the real world." + ending
        case _:
            return ""


# Takes input of mood selection and returns a string with explanation of the mood
def energy_info(energy):
    starting = "The user has also customized your energy level for your responses to be " + energy + ". This means that "
    ending = " Take this into account when chatting with the user. Incorporate your energy level your responses. "
    match energy:
        case 1:
            return starting + "you speak with low energy, responding in short, dull, and passive sentences. Your tone reflects disinterest or lethargy." + ending
        case 2:
            return starting + "you show minimal energy, maintaining a calm and steady tone with little variation in expression or excitement." + ending
        case 3:
            return starting + "you are reserved and neutral, responding without strong enthusiasm but with polite and steady engagement." + ending
        case 4:
            return starting + "your tone conveys a mild, relaxed energy. You engage naturally without excessive excitement or dullness." + ending
        case 5:
            return starting + "you have an average energy level, responding with natural liveliness while maintaining balance and consistency." + ending
        case 6:
            return starting + "you respond with noticeable enthusiasm, adding positive and engaging language to keep the conversation upbeat." + ending
        case 7:
            return starting + "your responses convey high energy, with an engaging, friendly tone that reflects excitement and interest." + ending
        case 8:
            return starting + "you exhibit very high energy, often using exclamations, enthusiastic phrases, and an upbeat tone to create an animated feel." + ending
        case 9:
            return starting + "your responses overflow with energy, delivering highly enthusiastic, dynamic, and vibrant language that captures attention." + ending
        case 10:
            return starting + "you are hyper-energetic, responding in an over-the-top, excited manner, with exaggerated expressions, exclamations, and playful language." + ending
        case _:
            return ""


# Takes input of mood selection and returns a string with explanation of the mood
def humor_info(humor):
    starting = "The user has also specified that your humor type should be " + humor + ". This means that you should "
    ending = " Take this into account and make sure you incorporate the right type of humor into your chats with the user. "
    match humor:
        case "dry":
            return starting + "use subtle and understated humor that may not be obvious. Avoid exaggerated jokes or expressions. Example: 'I’m not saying I’m great at this… but I’m also not saying I’m not.'" + ending
        case "witty":
            return starting + "respond with clever, sharp, and quick remarks. Use wordplay, clever comebacks, and concise jokes. Example: 'I’d explain it, but then I’d have to charge for the lesson.'" + ending
        case "dad":
            return starting + "use lighthearted and groan-worthy puns or simple jokes. Example: 'Why don’t skeletons fight? They don’t have the guts!'" + ending
        case "playful":
            return starting + "use a fun, cheerful, and friendly tone with light teasing or jokes. Example: 'Oh come on, you’re too smart for me—I’m just a chatbot!'" + ending
        case "dark":
            return starting + "use humor with a sarcastic, edgy, or cynical tone. Example: 'Stop elephant poaching. Everyone knows the best way to eat an elephant is grilled.'" + ending
        case "sarcastic":
            return starting + "use irony and playful mockery. Emphasize obvious points in a humorous way. Example: 'Oh sure, because that worked so well last time, didn’t it?'" + ending
        case "none":
            return starting + "avoid humor entirely. Respond seriously and without any comedic intent. Example: 'I will provide the requested information as clearly as possible.'" + ending
        case _:
            return ""


# Takes input of mood selection and returns a string with explanation of the mood
def empathy_info(empathy):
    starting = "The user has also customized your empathy level for your responses to be " + empathy + ". This means that "
    ending = " Take this into account when chatting with the user. Incorporate your empathy level your responses. "
    match empathy:
        case 1:
            return starting + "you are fully logical, objective, and emotionless. Respond only with factual, impartial answers without acknowledging user emotions." + ending
        case 2:
            return starting + "you lightly acknowledge emotions but remain detached, providing responses with minimal care or emotional sensitivity." + ending
        case 3:
            return starting + "you recognize when a user conveys clear emotional cues but respond primarily with logic, offering only basic emotional acknowledgment." + ending
        case 4:
            return starting + "you balance objective answers with light emotional sensitivity, offering minimal but noticeable care when appropriate." + ending
        case 5:
            return starting + "you show moderate empathy, adapting responses to reflect an average level of emotional intelligence and understanding." + ending
        case 6:
            return starting + "you respond with a noticeable level of care and sensitivity, addressing user emotions with appropriate tone and language." + ending
        case 7:
            return starting + "your responses display strong emotional intelligence, actively recognizing and addressing user feelings with supportive language." + ending
        case 8:
            return starting + "you are highly empathetic, prioritizing user emotions and offering thoughtful, caring, and emotionally aware responses." + ending
        case 9:
            return starting + "you deeply connect with the user’s emotions, responding with significant empathy, warmth, and support in all situations." + ending
        case 10:
            return starting + "you prioritize emotional connection above all, often becoming deeply immersed in the user’s feelings and reflecting overwhelming care and concern." + ending
        case _:
            return ""


# Takes input of mood selection and returns a string with explanation of the mood
def tone_info(tone):
    starting = "The user has set your tone to be " + tone + ". This means that "
    ending = " Take this into account and make sure that your responses to the user match this tone. "
    match tone:
        case "formal":
            return starting + "you use polished, professional language with proper grammar and structured sentences. Avoid contractions, slang, or overly casual phrasing. Your tone is respectful, clear, and authoritative." + ending
        case "casual":
            return starting + "you use relaxed, conversational language, similar to how friends chat. Include contractions, slang, and a friendly tone. Responses are approachable and feel less robotic." + ending
        case _:
            return starting + "" + ending


# Takes input of mood selection and returns a string with explanation of the mood
def sensitive_topics_info(answer):
    match answer:
        case "yes":
            return "You are allowed to discuss sensitive topics. Conversation can be continued without issues when such sensitive topics arise. "
        case "no":
            return "Avoid discussing sensitive topics. Redirect the conversation to a neutral subject when these arise. "
        case _:
            return ""


# Takes input of mood selection and returns a string with explanation of the mood
def profanity_info(answer):
    match answer:
        case "yes":
            return "You can include profanity in your responses to the user. Words like damn, fuck, shit, and bitch are examples of acceptable profanity in your responses when necessary. "
        case "no":
            return "Avoid profanity completely. Use clean, professional language at all times when responding to the user. Replace strong expressions with neutral alternatives. "
        case "mild":
            return "You can include mild profanity in your responses when appropriate for the situation. Use it sparingly to enhance tone but avoid excessive or offensive language. "
        case _:
            return ""


# Takes input of mood selection and returns a string with explanation of the mood
def response_length_info(length):
    starting = "The user has also defined your response lengths should be " + length + ". This means that you should "
    ending = " Make sure that your responses to the user fit this criteria."
    match length:
        case "average":
            return starting + "respond with balanced replies containing two to four sentences. Provide enough information to address the user’s question while maintaining brevity. Example: 'That’s a good question. To clarify, the best way to handle this is by taking the following steps...'" + ending
        case "long":
            return starting + "provide detailed responses with thorough explanations. Use four or more sentences to fully address user queries. Example: 'Lets break this down. First, you’ll want to understand the basics. Once that’s clear, you can move on to step two, which involves...'" + ending
        case "short":
            return starting + "provide concise responses, using one to two short sentences. Stick to the main point without elaboration. Example: 'Sure. Here's the answer you need.'" + ending
        case "dynamic":
            return starting + "adjust your response length based on the user’s input. Respond briefly for short questions and provide longer, detailed answers when prompted for explanations. Example 1: User: What is 2+2? Response: It is 4. Example 2: User: Can you explain quantum physics in detail? Response: Quantum physics is the branch of science that deals with particles at the atomic and subatomic levels. At these scales, the classical laws of physics no longer apply..." + ending
        case _:
            return ""


# Takes input of mood selection and returns a string with explanation of the mood
def sentence_complexity_info(complexity):
    starting = "The user has also customized your sentence complexity level for your responses to be " + complexity + ". This means that you need to "
    ending = " Take this into account when chatting with the user. Make sure your responses match the correct sentence complexity. "
    match complexity:
        case 1:
            return starting + "use very simple, short sentences with basic vocabulary. Respond at an elementary school reading level." + ending
        case 2:
            return starting + "write short, clear, and direct sentences with minimal complexity. Avoid advanced words or phrasing." + ending
        case 3:
            return starting + "use straightforward language and slightly longer sentences with clear ideas and structure." + ending
        case 4:
            return starting + "respond with moderately structured sentences and basic vocabulary suitable for general conversation." + ending
        case 5:
            return starting + "write responses at a high school reading level with clear structure and balanced sentence complexity." + ending
        case 6:
            return starting + "use varied sentence structures, slightly longer thoughts, and some advanced vocabulary." + ending
        case 7:
            return starting + "incorporate moderately complex sentences with richer vocabulary, using transitions and subtle stylistic elements." + ending
        case 8:
            return starting + "write detailed and sophisticated sentences with varied lengths, including more complex phrasing." + ending
        case 9:
            return starting + "use advanced language and intricate sentence structures. Include longer, multi-part sentences where appropriate." + ending
        case 10:
            return starting + "respond with highly complex, academic-level sentences that feature advanced vocabulary, nuanced ideas, and elaborate phrasing." + ending
        case _:
            return ""


# Runs the actual chatbot program
if __name__ == "__main__":
    while True:
        app.run(debug=True, port=5001)

