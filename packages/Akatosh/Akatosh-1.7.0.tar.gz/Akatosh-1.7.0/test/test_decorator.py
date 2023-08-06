from Akatosh import event, Mundus

@event()
def hail():
    print(f"{Mundus.now}:\tHail Akatosh!")

@event(on_call=True)
def dragon_shout(msg:str="Ros Fu Da!"):
    print(f"{Mundus.now}:\t{msg}")

dragon_shout()

Mundus.simulate(1)
