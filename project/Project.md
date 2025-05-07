# Dungeon Master AI Project

**Author:** Austin Turner

A Python-based AI Dungeon Master that runs as a networked turn-based server, guiding players through Dungeons & Dragons adventures with dynamic storytelling, dice-based mechanics, retrieval-augmented context, multi-step reasoning, and NPC image generation.

---

## Base System Functionality

**Overview:**  
The system starts up a DungeonMasterServer and one or more player clients. Each turn, the DM:
- Calls the LLM to narrate the next scene.
- Broadcasts the narrative to all connected clients.
- Waits for player actions.
- Processes tool calls (dice rolls and image generations).
- Advances the turn and updates game state.

**Scenarios Supported:**  
- **Tavern Social Encounters:** Introduce NPCs, dialogue branches, rumors.  
- **Exploration & Navigation:** Describe environments (villages, forests, ruins).  
- **Combat & Skill Checks:** Automated roll_dice for attacks, saves, stealth, etc.  
- **Puzzle & Trap Resolution:** Skill checks and branching narrative on success/failure.  
- **NPC Interaction & Portraits:** Introduce new characters with generated images.  
- **Loot & Inventory Decisions:** Handle player choices, though inventory is narrative-only.  

---

## Prompt Engineering & Model Parameters

**Model Parameters:**
- **Temperature:** 0.2
  - Ensures consistent, focused narration with slight creative flexibility.
- **Max Tokens:** 200
  - Adequate length for clear narration, reasoning steps, and dialogue without verbosity.

**Prompt Engineering Techniques:**
- Clearly defined Dungeon Master role in system prompt
- Explicit instructions for using tools such as dice rolls and NPC image generation

**Rationale:**  
The system prompt and parameters maintain narrative coherence and structured reasoning, clearly directing the DM to use specific tools at appropriate times.

---

## Tools Usage

The DM integrates several AI-driven tools:

- **Dice Rolling (roll_dice):**
- Uses the d20 library to parse and execute standard D&D dice notation.
- Provides detailed roll outcomes to players (including total and breakdown).

- **NPC Image Generation (generate_npc_image):**
- Uses Python's Pillow library to dynamically create placeholder NPC images.
- Enhances immersion by visually depicting characters based on textual descriptions.

- **Retrieval-Augmented Generation (RAG):**
- Implements ChromaDB and LangChain to manage detailed class information (classes_info.txt).
- Ensures consistent, accurate narrative context throughout gameplay.

---

## Planning & Reasoning

The AI demonstrates advanced multi-step reasoning capabilities:

- Implements explicit Chain-of-Thought (CoT) prompts instructing the model to:
- Consider environmental factors, character motivations, and narrative consistency before generating each turn's narrative.
- Use bullet-point reasoning internally (hidden from players) to ensure consistent logic.

- Example reasoning pattern:
    - Players are approaching an ancient ruin
    - The ruin contains hidden traps and a guarded artifact.
    - Describe initial visible details and prompt players for specific actions

---

## RAG Implementation

The system effectively incorporates Retrieval-Augmented Generation (RAG):

- **Context Management:**
- Utilizes a custom embedding function with Ollama to store and query detailed context in ChromaDB.
- Automatically retrieves relevant context (class information and environment details) based on player actions or narrative needs.

- **Integration:**
- When players take specific actions, the DM retrieves context to enhance the narrative.

---

## Additional Tools / Innovation

**NPC Image Generation with Pillow:**

- Automatically gets called upon first introduction of any new NPC
- Creates and saves PNG images depicting NPC descriptions

---

## Code Quality & Modular Design

The project has a clean, modular, and maintainable code design:

- **Modularity:**
- Separate modules with separate responsibilities:
  - `session_manager.py`: Manages the AI loop, tool calls, and RAG interactions
  - `dnd_dm.py`: Entry-point script
- Facilitates ease of debugging, enhancement, and feature addition

- **Documentation & Best Practices:**
- Descriptive comments
- Organized folder structure
