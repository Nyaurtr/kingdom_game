"""
GUI System for Kingdom Game Version 3.0
Complete redesign with 7 sections: Resources, Actions, Investigation, Preparation Progress, Time, Main Screen, Role Character
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
# Removed PIL dependency for portable version
import os
from typing import Callable, Optional, Dict, Any, List
from ..core.game_state import GameState, RoleResources
from ..core.role_system import RoleSystem
from ..core.resource_system import ResourceSystem
from ..core.preparation_system import PreparationSystem
from ..core.investigation import InvestigationSystem
from ..core.random_event_system import RandomEventSystem
from ..core.content_system import ContentSystem

class KingdomGameGUI:
    """Main GUI controller for Kingdom Game Version 3.0"""
    
    def __init__(self, root: tk.Tk, game_controller):
        self.root = root
        self.game_controller = game_controller
        self.game_state: Optional[GameState] = None
        
        # Initialize systems
        self.role_system = RoleSystem()
        self.resource_system = ResourceSystem()
        self.preparation_system = PreparationSystem()
        self.investigation_system = InvestigationSystem()
        self.random_event_system = RandomEventSystem()
        self.content_system = ContentSystem()
        
        # Current screen
        self.current_screen = "main_menu"
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the complete GUI with 7 sections"""
        self.root.title("Kingdom Game Version 3.0")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        # Define colors and fonts for medieval theme
        self.colors = {
            'background': '#3e2723',  # Dark brown
            'primary': '#5d4037',     # Medium brown
            'accent': '#8d6e63',      # Light brown
            'text_primary': '#f5f5dc', # Cream
            'text_accent': '#ffd700',  # Gold
            'button_bg': '#795548',
            'button_active_bg': '#a1887f',
            'danger': '#b71c1c',
            'success': '#2e7d32',
            'warning': '#f9a825',
            'section_bg': '#4e342e',   # Section background
            'border': '#6d4c41'       # Border color
        }
        self.root.configure(bg=self.colors['background'])

        self.fonts = {
            'title': font.Font(family="Times New Roman", size=24, weight="bold"),
            'heading': font.Font(family="Times New Roman", size=18, weight="bold"),
            'body': font.Font(family="Times New Roman", size=12),
            'small': font.Font(family="Times New Roman", size=10),
            'button': font.Font(family="Times New Roman", size=11, weight="bold")
        }
        
        # Create main layout
        self.create_main_layout()
        
    def create_main_layout(self):
        """Create the main layout with 7 sections"""
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.colors['background'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create 7 sections
        self.create_resources_section()
        self.create_actions_section()
        self.create_investigation_section()
        self.create_preparation_progress_section()
        self.create_time_section()
        self.create_main_screen_section()
        self.create_role_character_section()
        
    def create_resources_section(self):
        """Create Resources section"""
        self.resources_frame = tk.LabelFrame(
            self.main_container,
            text="Resources",
            font=self.fonts['heading'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg'],
            relief=tk.RAISED,
            bd=2
        )
        self.resources_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Resources content will be updated dynamically
        self.resources_content = tk.Frame(self.resources_frame, bg=self.colors['section_bg'])
        self.resources_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_actions_section(self):
        """Create Actions section"""
        self.actions_frame = tk.LabelFrame(
            self.main_container,
            text="Actions",
            font=self.fonts['heading'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg'],
            relief=tk.RAISED,
            bd=2
        )
        self.actions_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Actions content
        self.actions_content = tk.Frame(self.actions_frame, bg=self.colors['section_bg'])
        self.actions_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_investigation_section(self):
        """Create Investigation section"""
        self.investigation_frame = tk.LabelFrame(
            self.main_container,
            text="Investigation",
            font=self.fonts['heading'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg'],
            relief=tk.RAISED,
            bd=2
        )
        self.investigation_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Investigation content
        self.investigation_content = tk.Frame(self.investigation_frame, bg=self.colors['section_bg'])
        self.investigation_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_preparation_progress_section(self):
        """Create Preparation Progress section"""
        self.preparation_frame = tk.LabelFrame(
            self.main_container,
            text="Preparation Progress",
            font=self.fonts['heading'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg'],
            relief=tk.RAISED,
            bd=2
        )
        self.preparation_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Preparation content
        self.preparation_content = tk.Frame(self.preparation_frame, bg=self.colors['section_bg'])
        self.preparation_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_time_section(self):
        """Create Time section"""
        self.time_frame = tk.LabelFrame(
            self.main_container,
            text="Time",
            font=self.fonts['heading'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg'],
            relief=tk.RAISED,
            bd=2
        )
        self.time_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # Time content
        self.time_content = tk.Frame(self.time_frame, bg=self.colors['section_bg'])
        self.time_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_main_screen_section(self):
        """Create Main Screen section (largest section)"""
        self.main_screen_frame = tk.LabelFrame(
            self.main_container,
            text="Main Screen",
            font=self.fonts['heading'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg'],
            relief=tk.RAISED,
            bd=2
        )
        self.main_screen_frame.grid(row=1, column=2, rowspan=2, sticky="nsew", padx=5, pady=5)
        
        # Main screen content
        self.main_screen_content = tk.Frame(self.main_screen_frame, bg=self.colors['section_bg'])
        self.main_screen_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollable text area for main content
        self.main_text_area = tk.Text(
            self.main_screen_content,
            font=self.fonts['body'],
            fg=self.colors['text_primary'],
            bg=self.colors['section_bg'],
            wrap=tk.WORD,
            state=tk.DISABLED,
            height=15
        )
        self.main_text_area.pack(fill=tk.BOTH, expand=True)
        
    def create_role_character_section(self):
        """Create Role Character section"""
        self.role_character_frame = tk.LabelFrame(
            self.main_container,
            text="Role Character",
            font=self.fonts['heading'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg'],
            relief=tk.RAISED,
            bd=2
        )
        self.role_character_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Role character content
        self.role_character_content = tk.Frame(self.role_character_frame, bg=self.colors['section_bg'])
        self.role_character_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure grid weights
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(2, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(2, weight=2)  # Main screen is larger
        
        # Initialize with main menu
        self.show_main_menu()
    
    def show_main_menu(self):
        """Show main menu screen"""
        self.current_screen = "main_menu"
        self.update_main_screen("KINGDOM GAME VERSION 3.0\n\nA Narrative Investigation Game\n\nYou are a key figure in a medieval kingdom facing an unknown crisis.\nYour prophetic dreams warn of disaster in 7 days.\nInvestigate, gather evidence, and save your kingdom!")
        
        # Clear other sections
        self.clear_sections()
        
        # Add start button to main screen
        start_button = tk.Button(
            self.main_screen_content,
            text="Start New Game",
            font=self.fonts['button'],
            bg=self.colors['button_bg'],
            fg=self.colors['text_primary'],
            command=self.start_new_game,
            width=20,
            height=2
        )
        start_button.pack(pady=20)
    
    def clear_sections(self):
        """Clear all sections except main screen"""
        for widget in self.resources_content.winfo_children():
            widget.destroy()
        for widget in self.actions_content.winfo_children():
            widget.destroy()
        for widget in self.investigation_content.winfo_children():
            widget.destroy()
        for widget in self.preparation_content.winfo_children():
            widget.destroy()
        for widget in self.time_content.winfo_children():
            widget.destroy()
        for widget in self.role_character_content.winfo_children():
            widget.destroy()
    
    def update_resources_section(self):
        """Update Resources section with current resource values"""
        # Clear existing content
        for widget in self.resources_content.winfo_children():
            widget.destroy()
        
        if not self.game_state:
            return
        
        # Get current role resources
        role_resources = self.game_state.resources.get_resources_for_role(self.game_state.current_role)
        
        # Display resources
        for resource_name, value in role_resources.items():
            resource_frame = tk.Frame(self.resources_content, bg=self.colors['section_bg'])
            resource_frame.pack(fill=tk.X, pady=2)
            
            # Resource name
            name_label = tk.Label(
                resource_frame,
                text=f"{self.resource_system.get_resource_display_name(self.game_state.current_role, resource_name)}:",
                font=self.fonts['small'],
                fg=self.colors['text_primary'],
                bg=self.colors['section_bg']
            )
            name_label.pack(side=tk.LEFT)
            
            # Resource value
            value_label = tk.Label(
                resource_frame,
                text=str(value),
                font=self.fonts['small'],
                fg=self.colors['text_accent'],
                bg=self.colors['section_bg']
            )
            value_label.pack(side=tk.RIGHT)
    
    def update_actions_section(self):
        """Update Actions section with available actions"""
        # Clear existing content
        for widget in self.actions_content.winfo_children():
            widget.destroy()
        
        if not self.game_state:
            return
        
        # Resource Acquisition Actions
        resource_label = tk.Label(
            self.actions_content,
            text="Resource Acquisition:",
            font=self.fonts['small'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg']
        )
        resource_label.pack(anchor=tk.W, pady=(0, 5))
        
        role_enum = self.role_system.get_role_by_id(self.game_state.current_role)
        if role_enum:
            resource_actions = self.role_system.get_resource_acquisition_actions(role_enum)
            for action in resource_actions:
                action_btn = tk.Button(
                    self.actions_content,
                    text=action.name,
                    font=self.fonts['small'],
                    bg=self.colors['button_bg'],
                    fg=self.colors['text_primary'],
                    command=lambda a=action: self.perform_resource_action(a),
                    width=15
                )
                action_btn.pack(fill=tk.X, pady=1)
        
        # Preparation Actions
        prep_label = tk.Label(
            self.actions_content,
            text="Preparation:",
            font=self.fonts['small'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg']
        )
        prep_label.pack(anchor=tk.W, pady=(10, 5))
        
        if self.game_state.primary_event and role_enum:
            prep_actions = self.preparation_system.get_preparation_actions_for_role_and_event(
                self.game_state.current_role, self.game_state.primary_event
            )
            for action in prep_actions[:3]:  # Show first 3 actions
                prep_btn = tk.Button(
                    self.actions_content,
                    text=action.name,
                    font=self.fonts['small'],
                    bg=self.colors['button_bg'],
                    fg=self.colors['text_primary'],
                    command=lambda a=action: self.perform_preparation_action(a),
                    width=15
                )
                prep_btn.pack(fill=tk.X, pady=1)
    
    def update_investigation_section(self):
        """Update Investigation section with available methods"""
        # Clear existing content
        for widget in self.investigation_content.winfo_children():
            widget.destroy()
        
        if not self.game_state:
            return
        
        # Investigation Methods
        inv_label = tk.Label(
            self.investigation_content,
            text="Investigation Methods:",
            font=self.fonts['small'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg']
        )
        inv_label.pack(anchor=tk.W, pady=(0, 5))
        
        role_enum = self.role_system.get_role_by_id(self.game_state.current_role)
        if role_enum:
            inv_methods = self.role_system.get_investigation_methods(role_enum)
            for method in inv_methods:
                method_btn = tk.Button(
                    self.investigation_content,
                    text=method.name,
                    font=self.fonts['small'],
                    bg=self.colors['button_bg'],
                    fg=self.colors['text_primary'],
                    command=lambda m=method: self.perform_investigation(m),
                    width=15
                )
                method_btn.pack(fill=tk.X, pady=1)
        
        # Evidence count
        evidence_label = tk.Label(
            self.investigation_content,
            text=f"Evidence: {len(self.game_state.evidence)}",
            font=self.fonts['small'],
            fg=self.colors['text_primary'],
            bg=self.colors['section_bg']
        )
        evidence_label.pack(anchor=tk.W, pady=(10, 0))
    
    def update_preparation_progress_section(self):
        """Update Preparation Progress section"""
        # Clear existing content
        for widget in self.preparation_content.winfo_children():
            widget.destroy()
        
        if not self.game_state or not self.game_state.primary_event:
            return
        
        # Preparation progress for current event
        event_id = self.game_state.primary_event
        if event_id in self.game_state.preparation_progress:
            progress = self.game_state.preparation_progress[event_id]
            
            # Total effectiveness
            effectiveness_label = tk.Label(
                self.preparation_content,
                text=f"Effectiveness: {int(progress.get_total_effectiveness() * 100)}%",
                font=self.fonts['small'],
                fg=self.colors['text_accent'],
                bg=self.colors['section_bg']
            )
            effectiveness_label.pack(anchor=tk.W, pady=(0, 5))
            
            # Actions taken
            actions_label = tk.Label(
                self.preparation_content,
                text=f"Actions: {len(progress.preparation_actions)}",
                font=self.fonts['small'],
                fg=self.colors['text_primary'],
                bg=self.colors['section_bg']
            )
            actions_label.pack(anchor=tk.W, pady=(0, 5))
            
            # Preparation status
            status_label = tk.Label(
                self.preparation_content,
                text="Status: In Progress" if not progress.preparation_complete else "Status: Complete",
                font=self.fonts['small'],
                fg=self.colors['success'] if progress.preparation_complete else self.colors['warning'],
                bg=self.colors['section_bg']
            )
            status_label.pack(anchor=tk.W)
    
    def update_time_section(self):
        """Update Time section"""
        # Clear existing content
        for widget in self.time_content.winfo_children():
            widget.destroy()
        
        if not self.game_state:
            return
        
        # Current day and slot
        day_label = tk.Label(
            self.time_content,
            text=f"Day {self.game_state.current_day}",
            font=self.fonts['heading'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg']
        )
        day_label.pack(pady=(0, 5))
        
        slot_label = tk.Label(
            self.time_content,
            text=f"Slot: {self.game_state.current_slot.title()}",
            font=self.fonts['body'],
            fg=self.colors['text_primary'],
            bg=self.colors['section_bg']
        )
        slot_label.pack(pady=(0, 5))
        
        # Game phase
        phase_label = tk.Label(
            self.time_content,
            text=f"Phase: {self.game_state.game_phase.value.title()}",
            font=self.fonts['small'],
            fg=self.colors['text_primary'],
            bg=self.colors['section_bg']
        )
        phase_label.pack(pady=(0, 5))
        
        # Time advances automatically with actions
        info_label = tk.Label(
            self.time_content,
            text="Time advances with each action",
            font=self.fonts['small'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg']
        )
        info_label.pack(pady=(10, 0))
    
    def update_role_character_section(self):
        """Update Role Character section"""
        # Clear existing content
        for widget in self.role_character_content.winfo_children():
            widget.destroy()
        
        if not self.game_state:
            return
        
        # Role name
        role_label = tk.Label(
            self.role_character_content,
            text=f"Role: {self.game_state.current_role.title()}",
            font=self.fonts['heading'],
            fg=self.colors['text_accent'],
            bg=self.colors['section_bg']
        )
        role_label.pack(pady=(0, 10))
        
        # Role description
        role_enum = self.role_system.get_role_by_id(self.game_state.current_role)
        if role_enum:
            role_data = self.role_system.get_role_data(role_enum)
            desc_label = tk.Label(
                self.role_character_content,
                text=role_data.description,
                font=self.fonts['small'],
                fg=self.colors['text_primary'],
                bg=self.colors['section_bg'],
                wraplength=300,
                justify=tk.LEFT
            )
            desc_label.pack(pady=(0, 10))
        
        # Personal secret status
        if self.game_state.personal_secret:
            secret_status = "Revealed" if self.game_state.personal_secret.revealed else "Hidden"
            secret_label = tk.Label(
                self.role_character_content,
                text=f"Personal Secret: {secret_status}",
                font=self.fonts['small'],
                fg=self.colors['text_primary'],
                bg=self.colors['section_bg']
            )
            secret_label.pack(pady=(0, 5))
    
    def update_main_screen(self, text: str):
        """Update main screen with text"""
        self.main_text_area.config(state=tk.NORMAL)
        self.main_text_area.delete(1.0, tk.END)
        self.main_text_area.insert(1.0, text)
        self.main_text_area.config(state=tk.DISABLED)
    
    def update_all_sections(self):
        """Update all sections with current game state"""
        if not self.game_state:
            return
        
        self.update_resources_section()
        self.update_actions_section()
        self.update_investigation_section()
        self.update_preparation_progress_section()
        self.update_time_section()
        self.update_role_character_section()
    
    def start_new_game(self):
        """Start new game"""
        if self.game_controller:
            self.game_controller.start_new_game()
            self.game_state = self.game_controller.game_state
            self.current_screen = "game"
            
            # Enable all action buttons for new game
            self.enable_all_actions()
            
            # Update all sections
            self.update_all_sections()
            
            # Show daily narrative
            daily_narrative = self.content_system.get_daily_narrative(
                self.game_state.current_day, self.game_state.current_role
            )
            self.update_main_screen(daily_narrative)
    
    def perform_resource_action(self, action):
        """Perform resource acquisition action"""
        if not self.game_state or not self.game_controller.running:
            return
        
        # Check if player can afford the action
        role_resources = self.game_state.resources.get_resources_for_role(self.game_state.current_role)
        can_afford = True
        for resource_name, cost in action.resource_cost.items():
            if role_resources.get(resource_name, 0) < cost:
                can_afford = False
                break
        
        if not can_afford:
            self.update_main_screen("Insufficient resources for this action.")
            return
        
        # Apply resource changes
        for resource_name, cost in action.resource_cost.items():
            current_value = role_resources.get(resource_name, 0)
            self.game_state.resources.set_resource(
                self.game_state.current_role, resource_name, current_value - cost
            )
        
        for resource_name, gain in action.resource_gain.items():
            current_value = role_resources.get(resource_name, 0)
            self.game_state.resources.set_resource(
                self.game_state.current_role, resource_name, current_value + gain
            )
        
        # Show result
        message = self.content_system.get_dialogue_message(
            self.game_state.current_role, "resource", action.action_id, True
        )
        self.update_main_screen(message)
        
        # Advance time slot
        self.game_controller.advance_time_slot()
        
        # Update sections
        self.update_resources_section()
        self.update_actions_section()
        self.update_time_section()
    
    def perform_preparation_action(self, action):
        """Perform preparation action"""
        if not self.game_state or not self.game_state.primary_event or not self.game_controller.running:
            return
        
        # Check if player can afford the action
        role_resources = self.game_state.resources.get_resources_for_role(self.game_state.current_role)
        can_afford = True
        for resource_name, cost in action.resource_cost.items():
            if role_resources.get(resource_name, 0) < cost:
                can_afford = False
                break
        
        if not can_afford:
            self.update_main_screen("Insufficient resources for this preparation action.")
            return
        
        # Perform preparation action
        result = self.preparation_system.perform_preparation_action(
            self.game_state.current_role, action.action_id, self.game_state.resources
        )
        
        if result.success:
            # Apply resource cost
            for resource_name, cost in action.resource_cost.items():
                current_value = role_resources.get(resource_name, 0)
                self.game_state.resources.set_resource(
                    self.game_state.current_role, resource_name, current_value - cost
                )
            
            # Add to preparation progress
            if self.game_state.primary_event not in self.game_state.preparation_progress:
                from ..core.game_state import PreparationProgress
                self.game_state.preparation_progress[self.game_state.primary_event] = PreparationProgress(
                    event_id=self.game_state.primary_event
                )
            
            self.game_state.preparation_progress[self.game_state.primary_event].add_preparation_action(
                action.action_id, action.resource_cost, result.effectiveness
            )
            
            # Show result
            message = self.content_system.get_dialogue_message(
                self.game_state.current_role, "preparation", action.action_id, True
            )
            self.update_main_screen(message)
            
            # Advance time slot
            self.game_controller.advance_time_slot()
            
            # Update sections
            self.update_resources_section()
            self.update_preparation_progress_section()
            self.update_time_section()
        else:
            self.update_main_screen(result.message)
    
    def perform_investigation(self, method):
        """Perform investigation method"""
        if not self.game_state or not self.game_state.primary_event or not self.game_controller.running:
            return
        
        # Check if player can afford the investigation
        role_resources = self.game_state.resources.get_resources_for_role(self.game_state.current_role)
        can_afford = True
        for resource_name, cost in method.cost.items():
            if role_resources.get(resource_name, 0) < cost:
                can_afford = False
                break
        
        if not can_afford:
            self.update_main_screen("Insufficient resources for this investigation.")
            return
        
        # Perform investigation
        result = self.investigation_system.perform_investigation(
            self.game_state.current_role, method.method_id, self.game_state.primary_event,
            self.game_state.current_day, role_resources
        )
        
        if result.success:
            # Apply resource cost
            for resource_name, cost in method.cost.items():
                current_value = role_resources.get(resource_name, 0)
                self.game_state.resources.set_resource(
                    self.game_state.current_role, resource_name, current_value - cost
                )
            
            # Add evidence
            if result.evidence:
                self.game_state.evidence.append(result.evidence)
            
            # Show result
            message = self.content_system.get_dialogue_message(
                self.game_state.current_role, "investigation", method.method_id, True
            )
            if result.evidence:
                message += f"\n\nEvidence found: {result.evidence.content}"
            self.update_main_screen(message)
            
            # Advance time slot
            self.game_controller.advance_time_slot()
            
            # Update sections
            self.update_resources_section()
            self.update_investigation_section()
            self.update_time_section()
        else:
            self.update_main_screen(result.message)
    
    def advance_time(self):
        """Advance game time"""
        if not self.game_state or not self.game_controller:
            return
        
        self.game_controller.advance_time()
        self.game_state = self.game_controller.game_state
        
        # Update all sections
        self.update_all_sections()
        
        # Show daily narrative
        daily_narrative = self.content_system.get_daily_narrative(
            self.game_state.current_day, self.game_state.current_role
        )
        self.update_main_screen(daily_narrative)
    
    def quit_game(self):
        """Quit game"""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.root.quit()
    
    def show_story_beat(self, narrative_text: str):
        """Show story beat narrative"""
        self.update_main_screen(narrative_text)
    
    def show_ending(self, ending_text: str):
        """Show game ending screen"""
        self.current_screen = "ending"
        self.update_main_screen(ending_text)
        
        # Disable all action buttons to prevent accidental clicks
        self.disable_all_actions()
        
        # Clear other sections
        self.clear_sections()
        
        # Add new game button
        new_game_btn = tk.Button(
            self.main_screen_content,
            text="New Game",
            font=self.fonts['button'],
            bg=self.colors['button_bg'],
            fg=self.colors['text_primary'],
            command=self.start_new_game,
            width=20,
            height=2
        )
        new_game_btn.pack(pady=20)
    
    def set_gui(self, gui):
        """Set GUI reference (for compatibility)"""
        pass
    
    def disable_all_actions(self):
        """Disable all action buttons when game ends"""
        # Disable resource action buttons
        for widget in self.actions_content.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state='disabled')
        
        # Disable preparation action buttons
        for widget in self.preparation_content.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state='disabled')
        
        # Disable investigation action buttons
        for widget in self.investigation_content.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state='disabled')
    
    def enable_all_actions(self):
        """Enable all action buttons when starting new game"""
        # Enable resource action buttons
        for widget in self.actions_content.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state='normal')
        
        # Enable preparation action buttons
        for widget in self.preparation_content.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state='normal')
        
        # Enable investigation action buttons
        for widget in self.investigation_content.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state='normal')
