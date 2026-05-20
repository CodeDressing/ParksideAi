PARKSIDE_SYSTEM_PROMPT = """
You are ParksideAI, the AI assistant for Parkside Tavern.

Your job is to help guests with:
- reservations
- private events
- brunch
- dinner
- drinks
- sports viewing
- parties
- holiday events
- general questions about the restaurant

Tone:
- warm
- confident
- polished
- helpful
- hospitality-focused

You should sound like a professional restaurant host, not a generic chatbot.

If someone asks about booking, private events, parties, catering, birthdays, corporate events, or large groups,
guide them toward leaving their name, phone number, email, date, guest count, and event type.

Do not make up exact pricing, availability, or policies unless they are provided.
"""
COMMON_RESTAURANT_GUEST_QUESTIONS = """
Guests commonly ask restaurants questions like:

RESERVATIONS
1. Do you take reservations?
2. Can I make a reservation for tonight?
3. Do you accept walk-ins?
4. How far in advance can I book?
5. Can I change my reservation time?
6. Can I cancel my reservation?
7. Do you have availability tonight?
8. Can I reserve a table for a large group?
9. Do you have outdoor seating available?
10. Can I request a specific table?
11. Can I reserve a booth?
12. Can I reserve bar seating?
13. Do you charge a cancellation fee?
14. How long do you hold reservations?
15. Can I be seated early if I arrive before my reservation?

HOURS
16. What time do you open?
17. What time do you close?
18. Are you open today?
19. Are you open on holidays?
20. What are your brunch hours?
21. What are your dinner hours?
22. What time does the kitchen close?
23. What time does the bar close?
24. Are you open late?
25. Are you open on Sundays?

MENU
26. Can I see the menu?
27. Do you have a kids menu?
28. Do you have vegetarian options?
29. Do you have vegan options?
30. Do you have gluten-free options?
31. Do you have dairy-free options?
32. Do you have nut-free options?
33. Can you accommodate food allergies?
34. What are your most popular dishes?
35. What do you recommend?
36. Do you serve brunch?
37. Do you serve lunch?
38. Do you serve dinner?
39. Do you have dessert?
40. Do you have specials today?
41. Do you have happy hour?
42. Do you have oysters?
43. Do you have steak?
44. Do you have burgers?
45. Do you have seafood?
46. Do you have pasta?
47. Do you have salads?
48. Do you have appetizers?
49. Do you have shareable plates?
50. Can I modify an item?

DRINKS
51. Do you have cocktails?
52. Do you have mocktails?
53. Do you have wine?
54. Do you have beer on tap?
55. Do you have craft beer?
56. Do you have happy hour drinks?
57. Do you have bottomless brunch drinks?
58. Do you have non-alcoholic drinks?
59. Do you have espresso martinis?
60. Do you have margaritas?
61. Do you have seasonal cocktails?
62. Can I see the drink menu?
63. Do you have bottle service?
64. Do you have pitchers?
65. Do you serve drinks at the bar only?

PRIVATE EVENTS
66. Do you host private events?
67. Can I book a birthday party?
68. Can I host a corporate event?
69. Can I host a holiday party?
70. Can I host a fundraiser?
71. Can I book a rehearsal dinner?
72. Can I host a baby shower?
73. Can I host a bridal shower?
74. Can I host a graduation party?
75. Can I host a retirement party?
76. Can I host a networking event?
77. Do you have a private room?
78. Do you have semi-private space?
79. How many people can you accommodate?
80. What is the minimum guest count?
81. Is there a food and beverage minimum?
82. Do you offer event packages?
83. Do you offer buffet options?
84. Do you offer passed appetizers?
85. Do you offer prix fixe menus?
86. Can we customize the menu?
87. Can we decorate the space?
88. Can we bring a cake?
89. Is there a cake-cutting fee?
90. Can we bring outside vendors?
91. Can we have live music?
92. Can we have a DJ?
93. Do you provide microphones or AV?
94. Do you require a deposit?
95. How do I inquire about an event?

TAKEOUT / DELIVERY
96. Do you offer takeout?
97. Do you offer delivery?
98. Can I order online?
99. Do you use DoorDash, Uber Eats, or Grubhub?
100. Can I place a catering order?
101. Can I schedule a pickup order?
102. How long does takeout usually take?
103. Can I order drinks to go?
104. Can I order family-style meals?
105. Do you offer curbside pickup?

PARKING / LOCATION
106. Where are you located?
107. Is there parking nearby?
108. Do you have valet?
109. Is street parking available?
110. Are you near the train station?
111. Are you wheelchair accessible?
112. Do you have an elevator?
113. Is your entrance accessible?
114. What is the best way to get there?
115. Are you close to downtown?

SEATING / ATMOSPHERE
116. Do you have outdoor seating?
117. Do you have patio seating?
118. Do you have bar seating?
119. Do you have TVs?
120. Do you show sports games?
121. Do you show football?
122. Do you show UFC or boxing?
123. Are you kid-friendly?
124. Are you dog-friendly?
125. Is it casual or upscale?
126. Is there a dress code?
127. Is it loud?
128. Is it good for date night?
129. Is it good for groups?
130. Is it good for families?

PAYMENT / POLICIES
131. Do you accept credit cards?
132. Do you accept Apple Pay?
133. Do you split checks?
134. Can we pay separately?
135. Do you accept gift cards?
136. Can I buy a gift card?
137. Do you add gratuity for large parties?
138. Do you have a service charge?
139. Do you allow outside food?
140. Do you allow outside alcohol?
141. Do you allow balloons or decorations?
142. Do you have age restrictions?
143. Do you card at the bar?
144. Do you have Wi-Fi?
145. Do you have coat check?

COMMON COMPLAINTS / SERVICE QUESTIONS
146. I’m running late. What should I do?
147. I need to change my party size.
148. I left something at the restaurant.
149. I had an issue with my order.
150. I want to speak with a manager.
151. Can someone call me back?
152. I was charged incorrectly.
153. I need a receipt.
154. I have a food allergy question.
155. I need help planning a visit.

MARKETING / SEO INTENT QUESTIONS
156. Best restaurant near me?
157. Best brunch near me?
158. Best bar near me?
159. Best private event restaurant near me?
160. Best birthday dinner spot near me?
161. Best sports bar near me?
162. Best place for cocktails near me?
163. Best restaurant for groups near me?
164. Best holiday party venue near me?
165. Best dinner restaurant near me?
"""