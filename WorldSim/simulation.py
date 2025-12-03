import json

class Event:
    def __init__(self, event_type, entity_id=None, data=None):
        self.event_type = event_type
        self.entity_id = entity_id
        self.data = data or {}

class Entity:
    def __init__(self, id, type, x, y, health, props=None):
        self.id = id
        self.type = type
        self.x = x
        self.y = y
        self.health = health
        self.props = props or {}
        
class World:
    def __init__(self):
        self.entities = {}
        self.next_id = 1
        self.event_queue = {}
        self.tick = 0
        self.num_events = 0
        self.destroyed_entities= 0
        
    # ----------------
    #ENTITY MANAGEMENT
    #-----------------
    def spawn_entity(self, type, x, y, health=100, props=None):
        e = Entity(self.next_id, type, x, y, health, props)
        self.entities[self.next_id] = e
        self.next_id += 1
        return e
        
    #-----------------
    # EVENT SCHEDULING
    #-----------------
    def schedule_event(self, tick, event):
        if tick not in self.event_queue:
            self.event_queue[tick] = []
        self.event_queue[tick].append(event)
        
    #--------------
    #EVENT HANDLERS
    #--------------
    def handle_move(self, e, dx, dy):
        if dx > 0:
            e.x += 1
        elif dx < 0:
            e.x -= 1
        
        if dy > 0:
            e.y += 1
        elif dy < 0:
            e.y -= 1
            
    def handle_damage(self, e, amount):
        e.health -= amount
        if e.health <= 0:
            del self.entities[e.id]
            self.destroyed_entities += 1
            
    #--------------------
    #MAIN SIMULATION LOOP
    #--------------------
    def run(self, max_ticks=50):
        for _ in range(max_ticks):
            print(f"\n=== Tick {self.tick} ===")
            
            #process events for this tick
            events = self.event_queue.get(self.tick, [])
            for event in events:
                self.process_event(event)
                self.num_events += 1
            
            self.print_state()
            
            self.tick += 1
            
        alive = len(self.entities)
        total_health = sum(e.health for e in self.entities.values())
        
        print(f"Total ticks processed: {self.tick}")
        print(f"Number of events handled: {self.num_events}")
        print(f"Total entities alive: {alive}")
        print(f"Total entities destroyed: {self.destroyed_entities}")
        
        if alive > 0:
            avg_health = total_health/alive
            print(f"Average health of entities: {avg_health}")
            
    def process_event(self, event):
        # handle spawn first (no existing entity needed)
        if event.event_type == "spawn":
            spawn_data = event.data
            self.spawn_entity(
                spawn_data["type"],
                spawn_data["x"],
                spawn_data["y"],
                spawn_data.get("health", 100)
            )
            return

        # for all other events, we need a valid entity
        if event.entity_id not in self.entities:
            return

        e = self.entities[event.entity_id]

        if event.event_type == "move":
            dx = event.data.get("dx", 0)
            dy = event.data.get("dy", 0)
            self.handle_move(e, dx, dy)

        elif event.event_type == "damage":
            amount = event.data.get("amount", 0)
            self.handle_damage(e, amount)
            
    def print_state(self):
        for e in self.entities.values():
            print(f"Entity {e.id}: type={e.type}, pos=({e.x},{e.y}), health={e.health}")
            
    # --------------------
    # SAVE WORLD
    # --------------------
    def save_world(self, filename):
        data = {
            "destroyed_entities": self.destroyed_entities,
            "num_events": self.num_events,
            "tick": self.tick,
            "next_id": self.next_id,
            "entities": {},
            "event_queue": {}
        }

        # save entities
        for eid, e in self.entities.items():
            data["entities"][eid] = {
                "type": e.type,
                "x": e.x,
                "y": e.y,
                "health": e.health,
                "props": e.props
            }

        # save event queue
        for t, events in self.event_queue.items():
            data["event_queue"][t] = [
                {
                    "event_type": ev.event_type,
                    "entity_id": ev.entity_id,
                    "data": ev.data
                }
                for ev in events
            ]

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"World saved to {filename}")

    # --------------------
    # LOAD WORLD
    # --------------------
    def load_world(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)

        # reset world
        self.num_events = data["num_events"]
        self.destroyed_entities = data["destroyed_entities"]
        self.tick = data["tick"]
        self.next_id = data["next_id"]
        self.entities = {}
        self.event_queue = {}

        # load entities
        for eid, info in data["entities"].items():
            eid = int(eid)
            e = Entity(
                id=eid,
                type=info["type"],
                x=info["x"],
                y=info["y"],
                health=info["health"],
                props=info["props"]
            )
            self.entities[eid] = e

        # load events
        from simulation import Event  # avoids circular import if needed
        for t, events in data["event_queue"].items():
            t = int(t)
            self.event_queue[t] = [
                Event(ev["event_type"], ev["entity_id"], ev["data"])
                for ev in events
            ]

        print(f"World loaded from {filename}")
