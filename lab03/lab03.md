# Prompt Engineering Process
### Step 1
#### Intention
>What is the improvement that you intend to make?
1. For my first attempt, I wanted to use the same hyperparameters from the demo agent while changing the system prompt to give the agent the role of being a dungeon master.
    I did this to get a general sense of how the model would respond so that I could get a better understanding of what I wanted it to improve on. After doing this, I realized that I wanted the model to generally be more creative.
2. For my second attempt, I wanted the model to be much more efficient, since it is currently taking 3 or more minutes to generate each response.

#### Action/Change
>Why do you think this action/change will improve the agent?
1. To make the model more creative, I increased the temperature from 0.5 to 0.7 and increased the max number of tokens from 100 to 110. Modifying these hyperparameters should allow the model to have less predictive responses with a more relaxed decision-making process and potentially generate slightly longer responses when appropriate.
2. To reduce the time for response generation, I will reduce the max tokens from 110 to 50. This should make the model more efficient.

#### Result
>What was the result?
1. The model slightly improved, as expected (more creative with slightly longer responses) but the response generation time increased significantly.
2. The response generationg time was not improved. It still too 3-5 minutes for each response to be generated.

#### Reflection/Analysis of the result. 
>Why do you think it did or did not work?
1. I think my methods worked due to the increase in temperature and max tokens. However, I think the increase in max tokens is what caused the longer response generation time.
2. I think the poor response generation time has more to do with the performance of the virtual machine rather than the performance of the model. If I were running this program on a system with better specs, the performance would likely improve significantly.