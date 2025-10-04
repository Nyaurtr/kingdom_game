"""
Main game controller and entry point for Kingdom Game Version 3.0
Integrates all new systems: Resource, Preparation, Investigation, Random Events, Content
"""

from src.core.game_state import GameState, GamePhase
from src.core.role_system import RoleSystem, Role
from src.core.resource_system import ResourceSystem
from src.core.preparation_system import PreparationSystem
from src.core.investigation import InvestigationSystem
from src.core.random_event_system import RandomEventSystem
from src.core.content_system import ContentSystem
from src.ui.gui import KingdomGameGUI
import random
from typing import Optional

class KingdomGame:
    """Main game controller for Kingdom Game Version 3.0"""
    
    def __init__(self):
        self.game_state = GameState()
        self.role_system = RoleSystem()
        self.resource_system = ResourceSystem()
        self.preparation_system = PreparationSystem()
        self.investigation_system = InvestigationSystem()
        self.random_event_system = RandomEventSystem()
        self.content_system = ContentSystem()
        self.running = False
        self.gui = None
    
    def start_new_game(self) -> None:
        """Start a new game with random role assignment and event selection"""
        # Reset time to day 1, morning
        self.game_state.current_day = 1
        self.game_state.current_slot = "morning"
        
        # Random role assignment
        selected_role = self.role_system.get_random_role()
        self.game_state.current_role = selected_role.value
        
        # Initialize personal secret
        role_data = self.role_system.get_role_data(selected_role)
        from src.core.game_state import PersonalSecret
        self.game_state.personal_secret = PersonalSecret(
            secret_id=role_data.personal_secret.secret_id,
            revealed=False,
            impact_level=0.0,
            resolution_status="hidden"
        )
        
        # Initialize primary event (random from all 8 events)
        primary_events = [
            "famine_cascade", 
            "pandemic_surge", 
            "invasion_rebellion",
            "cult_uprising",
            "environmental_catastrophe",
            "crop_blight",
            "economic_collapse",
            "supernatural_rift"
        ]
        self.game_state.primary_event = random.choice(primary_events)
        
        # Set initial game phase
        self.game_state.game_phase = GamePhase.ACT_I
        
        # Initialize resources (already done in GameState default)
        # Resources start at 50 for all roles
        
        # Initialize preparation progress
        self.game_state.preparation_progress = {}
        
        # Initialize random events
        self.game_state.active_random_events = []
        self.game_state.random_event_history = []
        
        # Clear evidence and actions
        self.game_state.evidence = []
        self.game_state.actions_taken = []
        
        self.running = True
    
    def advance_time_slot(self) -> None:
        """Advance one time slot (morning -> afternoon -> evening -> next day morning)"""
        time_progression = {
            ("morning", 1): ("afternoon", 1),
            ("afternoon", 1): ("evening", 1),
            ("evening", 1): ("morning", 2),
            ("morning", 2): ("afternoon", 2),
            ("afternoon", 2): ("evening", 2),
            ("evening", 2): ("morning", 3),
            ("morning", 3): ("afternoon", 3),
            ("afternoon", 3): ("evening", 3),
            ("evening", 3): ("morning", 4),
            ("morning", 4): ("afternoon", 4),
            ("afternoon", 4): ("evening", 4),
            ("evening", 4): ("morning", 5),
            ("morning", 5): ("afternoon", 5),
            ("afternoon", 5): ("evening", 5),
            ("evening", 5): ("morning", 6),
            ("morning", 6): ("afternoon", 6),
            ("afternoon", 6): ("evening", 6),
            ("evening", 6): ("morning", 7),
            ("morning", 7): ("afternoon", 7),
            ("afternoon", 7): ("evening", 7),
            ("evening", 7): ("epilogue", 7)  # Game ends
        }
        
        current_key = (self.game_state.current_slot, self.game_state.current_day)
        if current_key in time_progression:
            new_slot, new_day = time_progression[current_key]
            self.game_state.current_slot = new_slot
            self.game_state.current_day = new_day
            
            # Update game phase based on day
            if new_day <= 2:
                self.game_state.game_phase = GamePhase.ACT_I
            elif new_day <= 4:
                self.game_state.game_phase = GamePhase.ACT_II
            elif new_day <= 6:
                self.game_state.game_phase = GamePhase.ACT_III
            else:
                self.game_state.game_phase = GamePhase.EPILOGUE
            
            # Check for random events
            self.check_random_events()
            
            # Check for game end
            if new_slot == "epilogue":
                self.end_game()
    
    def advance_time(self) -> None:
        """Advance game time (day/slot progression) with random events"""
        time_progression = {
            ("morning", 1): ("afternoon", 1),
            ("afternoon", 1): ("evening", 1),
            ("evening", 1): ("morning", 2),
            ("morning", 2): ("afternoon", 2),
            ("afternoon", 2): ("evening", 2),
            ("evening", 2): ("morning", 3),
            ("morning", 3): ("afternoon", 3),
            ("afternoon", 3): ("evening", 3),
            ("evening", 3): ("morning", 4),
            ("morning", 4): ("afternoon", 4),
            ("afternoon", 4): ("evening", 4),
            ("evening", 4): ("morning", 5),
            ("morning", 5): ("afternoon", 5),
            ("afternoon", 5): ("evening", 5),
            ("evening", 5): ("morning", 6),
            ("morning", 6): ("afternoon", 6),
            ("afternoon", 6): ("evening", 6),
            ("evening", 6): ("morning", 7),
            ("morning", 7): ("afternoon", 7),
            ("afternoon", 7): ("evening", 7),
            ("evening", 7): ("epilogue", 7)  # Game ends
        }
        
        current_key = (self.game_state.current_slot, self.game_state.current_day)
        if current_key in time_progression:
            new_slot, new_day = time_progression[current_key]
            self.game_state.current_slot = new_slot
            self.game_state.current_day = new_day
            
            # Update game phase based on day
            if new_day <= 2:
                self.game_state.game_phase = GamePhase.ACT_I
            elif new_day <= 4:
                self.game_state.game_phase = GamePhase.ACT_II
            elif new_day <= 6:
                self.game_state.game_phase = GamePhase.ACT_III
            else:
                self.game_state.game_phase = GamePhase.EPILOGUE
            
            # Check for random events
            self.check_random_events()
            
            # Check for game end
            if new_slot == "epilogue":
                self.end_game()
    
    def check_random_events(self):
        """Check for random events and apply them"""
        # Check if random event should trigger
        if self.random_event_system.should_trigger_random_event(self.game_state.current_day):
            # Check if we haven't exceeded max events
            if not self.random_event_system.is_max_events_reached(self.game_state.random_event_history):
                # Generate random event
                random_event = self.random_event_system.generate_random_event(
                    self.game_state.current_day, self.game_state.current_slot
                )
                
                if random_event:
                    # Apply event effects to resources
                    role_resources = self.game_state.resources.get_resources_for_role(self.game_state.current_role)
                    effects_applied = self.random_event_system.apply_random_event_effects(
                        random_event, self.game_state.resources, self.game_state.current_role
                    )
                    
                    # Add to history
                    self.game_state.random_event_history.append(random_event)
                    
                    # Show event message in GUI
                    if self.gui:
                        event_message = self.content_system.get_random_event_message(
                            random_event.event_id, self.game_state.current_role
                        )
                        self.gui.update_main_screen(f"Random Event: {event_message}")
    
    def end_game(self) -> None:
        """End the game and determine ending based on preparation effectiveness"""
        if not self.game_state.primary_event:
            return
        
        # Generate comprehensive ending report
        ending_report = self._generate_ending_report()
        
        # Show ending in GUI
        if self.gui:
            self.gui.show_ending(ending_report)
        
        self.running = False
    
    def _generate_ending_report(self) -> str:
        """Generate comprehensive ending report with all game details"""
        report = []
        
        # Header
        report.append("=" * 60)
        report.append("KINGDOM CRISIS RESOLUTION REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Role and Event Information
        role_name = self.game_state.current_role.title()
        event_name = self.game_state.primary_event.replace("_", " ").title()
        report.append(f"Role: {role_name}")
        report.append(f"Crisis Event: {event_name}")
        report.append(f"Final Day: {self.game_state.current_day}")
        report.append("")
        
        # Evidence Collected
        report.append("EVIDENCE COLLECTED:")
        report.append("-" * 30)
        if self.game_state.evidence:
            for i, evidence in enumerate(self.game_state.evidence, 1):
                report.append(f"{i}. {evidence.content}")
                report.append(f"   Reliability: {evidence.reliability.title()}")
                report.append(f"   Source: {evidence.source_type.title()}")
                report.append(f"   Location: {evidence.location}")
                report.append("")
        else:
            report.append("No evidence was collected during the investigation.")
            report.append("")
        
        # Preparation Actions Taken
        report.append("PREPARATION ACTIONS TAKEN:")
        report.append("-" * 30)
        if self.game_state.primary_event in self.game_state.preparation_progress:
            prep_progress = self.game_state.preparation_progress[self.game_state.primary_event]
            if prep_progress.preparation_actions:
                for i, (action_id, action_data) in enumerate(prep_progress.preparation_actions.items(), 1):
                    report.append(f"{i}. {action_id.replace('_', ' ').title()}")
                    report.append(f"   Resource Cost: {action_data['resource_cost']}")
                    report.append(f"   Effectiveness: {action_data['effectiveness']:.1%}")
                    report.append("")
            else:
                report.append("No preparation actions were taken.")
                report.append("")
        else:
            report.append("No preparation was made for this crisis.")
            report.append("")
        
        # Resource Status
        report.append("FINAL RESOURCE STATUS:")
        report.append("-" * 30)
        resources = self.game_state.resources.get_resources_for_role(self.game_state.current_role)
        for resource_name, value in resources.items():
            report.append(f"{resource_name.replace('_', ' ').title()}: {value}")
        report.append("")
        
        # Random Events
        report.append("RANDOM EVENTS ENCOUNTERED:")
        report.append("-" * 30)
        if self.game_state.random_event_history:
            for i, event in enumerate(self.game_state.random_event_history, 1):
                report.append(f"{i}. {event.name} (Day {event.day}, {event.slot})")
                report.append(f"   {event.description}")
                report.append("")
        else:
            report.append("No random events occurred during this crisis.")
            report.append("")
        
        # Crisis Resolution
        report.append("CRISIS RESOLUTION:")
        report.append("-" * 30)
        if self.game_state.primary_event in self.game_state.preparation_progress:
            preparation_progress = self.game_state.preparation_progress[self.game_state.primary_event]
            crisis_resolution = self.preparation_system.calculate_crisis_resolution(
                self.game_state.primary_event, preparation_progress
            )
            
            report.append(f"Preparation Effectiveness: {crisis_resolution['effectiveness']:.1%}")
            report.append(f"Actions Taken: {crisis_resolution['preparation_actions']}")
            report.append("")
            
            # Get ending message
            ending_message = self.content_system.get_ending_message(
                self.game_state.primary_event, crisis_resolution["outcome"], self.game_state.current_role
            )
            report.append("FINAL OUTCOME:")
            report.append("-" * 30)
            report.append(ending_message)
        else:
            report.append("No preparation was made for this crisis.")
            report.append("")
            report.append("FINAL OUTCOME:")
            report.append("-" * 30)
            ending_message = self.content_system.get_ending_message(
                self.game_state.primary_event, "kingdom_falls", self.game_state.current_role
            )
            report.append(ending_message)
        
        report.append("")
        report.append("=" * 60)
        report.append("END OF REPORT")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def set_gui(self, gui):
        """Set GUI reference"""
        self.gui = gui