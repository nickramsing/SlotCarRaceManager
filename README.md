# PROBLEM



# Solution Vision

## Initial prompt 
You are an applied mathematician familiar with optimization problems. You are also a skilled hobbyist that races complex slot cars (such as scalextric slot cars) in fun, but highly competitive races. You are interested in ensuring races you host are fair and equitable. That is already challenging given that drivers possess different skills and levels of experiences and the slot cars do not perform exactly the same. You are hosting a race competition as the race director. The race competition is composed of a series of race events where You need to generate You want participants to all have fair chances per the following specifications: 1. You are constrained by having 6 cars: you can identify cars by their colors [Red, Green, Blue, Yellow, Orange, White]. 2. You have 18 drivers: you can label drivers D1 - D18 3. The race course can accommodate all 6 cars. So, each race event on the race course may have 6 drivers maximum. 4. Each driver must use each car (color) exactly once. This ensures equity with cars: everyone will have used each car. 5. Every driver must race other driver at least once but no more than twice. You must minimize the number of times drivers race against each other but you must ensure that everyone races each other. Can you construct a race schedule that ensures equity, but does not require endless race events? I want participants to be competitive, have fun, but not be board!
- Objective:
  - Minimize heats
  - Minimize wasted slots

## Technical Solution: true optimization / constraint-satisfaction model. 
- 6 cars / slots per heat
- Drivers must use each car once
- Some heats may be partially filled
- We want minimum number of heats and minimum wasted slots
- Every pair must meet ≥ 1 and ≤ 2 times
-Below is a true optimizer-style solver using backtracking + pruning. It will:
  - Work for 6, 12, 15, 18, … drivers
  - Minimizes number of heats
  - Minimizes wasted slots
  - Allows partially-filled heats (not full 6 lanes)
  - Enforces:
    - each driver uses each car exactly once
    - max 6 drivers per heat
    - pair constraints: no pair meets more than twice
    - every pair meets at least once

## Iterations
1. Scenario 1
   1. Objectives:
      1. Minimize heats 
      1. Minimize wasted slots
   1. Outcomes:
      1. Works!  Meets current objectives 
      2. But some drivers need to wait for several heats before racing again
1. Scenario 2
   1. Objectives:
      1. Minimize heats 
      1. Minimize wasted slots
      2. Minimize waiting time for drivers between heats
   3. Outcomes:
 
# Learnings

## InContext Learning
### Create a dedicated Agent to assess, validate, and modify the race schedule creation logic
1.  CLAUDE.md vs. Specialized Agent File                                                                                                                                      
                                                                                                                                                                            
-  Both are valuable, serving different purposes:                                                                                                                            
  ┌──────────────────────────┬───────────────────────────────────────────────┐                                                                                              
  │        CLAUDE.md         │ Specialized Agent (e.g., OPTIMIZER_AGENT.md)  │                                                                                              
  ├──────────────────────────┼───────────────────────────────────────────────┤                                                                                              
  │ General project guidance │ Deep domain expertise                         │                                                                                              
  ├──────────────────────────┼───────────────────────────────────────────────┤                                                                                              
  │ Architecture overview    │ Mathematical formulations & OR-Tools patterns │                                                                                              
  ├──────────────────────────┼───────────────────────────────────────────────┤                                                                                              
  │ Build commands           │ Optimization trade-off reasoning              │                                                                                              
  ├──────────────────────────┼───────────────────────────────────────────────┤                                                                                              
  │ Broad scope              │ Focused on create_race_schedule.py            │                                                                                              
  └──────────────────────────┴───────────────────────────────────────────────┘                                                                                              
-  Recommendation: Keep CLAUDE.md as-is for general project context. Create a separate OPTIMIZER_AGENT.md that you can reference when working specifically on schedule       
  optimization. You can invoke it by asking Claude Code to "use the optimizer agent persona" or by including it in context.                                                 
                                                                                                                                                                            
2. Summary of Objectives for the Agent                                                                                                                                       
                                                                                                                                                                            
- The agent should optimize for:                                                                                                                     
                                                                                                                                                                            
  1. Car equity: Every driver races each car exactly once ✓ (existing)                                                                                                      
  2. Pairing equity: Every driver pair meets 1-2 times ✓ (existing)                                                                                                         
  3. Engagement: No driver sits idle for more than 3 consecutive heats ⚡ (new constraint)                                                                                  
  4. Flexibility: Handle variable driver/car/slot counts ⚡ (enhancement)                                                                                                   
  5. Minimize heats + wasted slots ✓ (existing objective)                                                                                                                   
                                                                                                                                                                             
- It will include:                                                                                             
  - The three-perspective persona (mathematician, developer, hobbyist)                                                                                                      
  - Current constraint model documentation                                                                                                                                  
  - The new idle-time constraint requirement                                                                                                                                
  - Guidance for evaluating and improving the solver   
- 

# To Dos:
1. Add logging: [DONE]
   1. create a logging module to handle logs - DONE
   2. define a custom log message format - DONE 
   3. send log message to log_writer - DONE
   4. Add logging to services
      1. create_race_schedule.py - to do
      2. publish_schedule.py - DONE

2. video to review: https://www.youtube.com/watch?v=pxuXaaT1u3k