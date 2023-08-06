# Akatosh
This is a light weighted disceret event simulation library. The name is from the Dragon God of Time in Elder Scroll. :)

# Install
    pip install --upgrade Akatosh
  
## How to use
Import modules:

    from Akatosh import Mundus, Actor
    
create actors, aka event:

There are serveral ways that you can create an event:
1. Create an event with lambda expression
    
        Actor(action = lambda: print("All hail dragonborn!"))
        
2. Create an event with defined functions:

        #funtion without arguments
        def hail():
            print("All hail dragonborn!")
        Actor(action = hail)
        
        #function with arguments
        def hail(message: str):
            print(message)
        Actor(action = hail, message = "All hail dragonborn!")
 
3. Create an event by subclass:
 
         class Myevent(Actor):

            def action(self):
                print("All hail dragonborn!")

         Myevent()

4. Create with decorator (new!)

        #directly create an event with a function:
        @event()
        def hail():
            print(f"{Mundus.now}:\tHail Akatosh!")       

        #create a on call event, that is the decorated function must be called to actually make the event
        @event(on_call=True)
        def dragon_shout(msg:str="Ros Fu Da!"):
            print(f"{Mundus.now}:\t{msg}")
         
 To start the simulation,
 
        Mundus.simulate(till=inf)
