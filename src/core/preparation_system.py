"""
Preparation system for Kingdom Game Version 3.0
Handles preparation actions, effectiveness calculation, and crisis resolution
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from .game_config import PREPARATION_THRESHOLDS, GAME_CONFIG
from .game_state import PreparationProgress, RoleResources

@dataclass
class PreparationAction:
    """A preparation action for a specific event"""
    action_id: str
    name: str
    description: str
    resource_cost: Dict[str, int]
    effectiveness_level: str  # "high", "medium", "low"
    base_effectiveness: float
    event_id: str
    role: str

@dataclass
class PreparationResult:
    """Result of a preparation action"""
    success: bool
    effectiveness: float
    resource_cost: Dict[str, int]
    message: str
    threshold_met: bool

class PreparationSystem:
    """Manages preparation actions and effectiveness calculation"""
    
    def __init__(self):
        self.thresholds = PREPARATION_THRESHOLDS
        self.game_config = GAME_CONFIG
        self.preparation_actions = self._initialize_preparation_actions()
    
    def _initialize_preparation_actions(self) -> Dict[str, List[PreparationAction]]:
        """Initialize all preparation actions for all events and roles"""
        actions = {}
        
        # King preparation actions
        actions["king"] = self._get_king_preparation_actions()
        
        # Captain preparation actions  
        actions["captain"] = self._get_captain_preparation_actions()
        
        # Spy preparation actions
        actions["spy"] = self._get_spy_preparation_actions()
        
        return actions
    
    def _get_king_preparation_actions(self) -> List[PreparationAction]:
        """Get King preparation actions for all events"""
        return [
            # Famine Cascade
            PreparationAction("king_famine_emergency_food", "Emergency Food Distribution", 
                            "High cost, high effectiveness", {"treasury": 30, "food_reserves": 20}, 
                            "high", 0.8, "famine_cascade", "king"),
            PreparationAction("king_famine_agricultural_investment", "Agricultural Investment", 
                            "Medium cost, medium effectiveness", {"treasury": 20, "food_reserves": 15}, 
                            "medium", 0.6, "famine_cascade", "king"),
            PreparationAction("king_famine_trade_embargo", "Trade Embargo Lifting", 
                            "Low cost, low effectiveness", {"treasury": 10, "food_reserves": 10}, 
                            "low", 0.4, "famine_cascade", "king"),
            
            # Pandemic Surge
            PreparationAction("king_pandemic_medical_infrastructure", "Medical Infrastructure", 
                            "High cost, high effectiveness", {"treasury": 30, "public_trust": 20}, 
                            "high", 0.8, "pandemic_surge", "king"),
            PreparationAction("king_pandemic_quarantine_protocols", "Quarantine Protocols", 
                            "Medium cost, medium effectiveness", {"treasury": 20, "public_trust": 15}, 
                            "medium", 0.6, "pandemic_surge", "king"),
            PreparationAction("king_pandemic_healer_recruitment", "Healer Recruitment", 
                            "Low cost, low effectiveness", {"treasury": 10, "public_trust": 10}, 
                            "low", 0.4, "pandemic_surge", "king"),
            
            # Invasion Rebellion
            PreparationAction("king_invasion_military_funding", "Military Funding", 
                            "High cost, high effectiveness", {"treasury": 30, "noble_support": 20}, 
                            "high", 0.8, "invasion_rebellion", "king"),
            PreparationAction("king_invasion_defense_fortification", "Defense Fortification", 
                            "Medium cost, medium effectiveness", {"treasury": 20, "noble_support": 15}, 
                            "medium", 0.6, "invasion_rebellion", "king"),
            PreparationAction("king_invasion_diplomatic_outreach", "Diplomatic Outreach", 
                            "Low cost, low effectiveness", {"treasury": 10, "noble_support": 10}, 
                            "low", 0.4, "invasion_rebellion", "king"),
            
            # Cult Uprising
            PreparationAction("king_cult_religious_reforms", "Religious Reforms", 
                            "High cost, high effectiveness", {"treasury": 30, "public_trust": 20}, 
                            "high", 0.8, "cult_uprising", "king"),
            PreparationAction("king_cult_investigation", "Cult Investigation", 
                            "Medium cost, medium effectiveness", {"treasury": 20, "public_trust": 15}, 
                            "medium", 0.6, "cult_uprising", "king"),
            PreparationAction("king_cult_public_education", "Public Education", 
                            "Low cost, low effectiveness", {"treasury": 10, "public_trust": 10}, 
                            "low", 0.4, "cult_uprising", "king"),
            
            # Environmental Catastrophe
            PreparationAction("king_environmental_disaster_preparedness", "Disaster Preparedness", 
                            "High cost, high effectiveness", {"treasury": 30, "food_reserves": 20}, 
                            "high", 0.8, "environmental_catastrophe", "king"),
            PreparationAction("king_environmental_evacuation_plans", "Evacuation Plans", 
                            "Medium cost, medium effectiveness", {"treasury": 20, "food_reserves": 15}, 
                            "medium", 0.6, "environmental_catastrophe", "king"),
            PreparationAction("king_environmental_resource_stockpiling", "Resource Stockpiling", 
                            "Low cost, low effectiveness", {"treasury": 10, "food_reserves": 10}, 
                            "low", 0.4, "environmental_catastrophe", "king"),
            
            # Crop Blight
            PreparationAction("king_crop_seed_distribution", "Seed Distribution", 
                            "High cost, high effectiveness", {"treasury": 30, "food_reserves": 20}, 
                            "high", 0.8, "crop_blight", "king"),
            PreparationAction("king_crop_agricultural_research", "Agricultural Research", 
                            "Medium cost, medium effectiveness", {"treasury": 20, "food_reserves": 15}, 
                            "medium", 0.6, "crop_blight", "king"),
            PreparationAction("king_crop_farmer_support", "Farmer Support", 
                            "Low cost, low effectiveness", {"treasury": 10, "food_reserves": 10}, 
                            "low", 0.4, "crop_blight", "king"),
            
            # Economic Collapse
            PreparationAction("king_economic_reforms", "Economic Reforms", 
                            "High cost, high effectiveness", {"treasury": 30, "noble_support": 20}, 
                            "high", 0.8, "economic_collapse", "king"),
            PreparationAction("king_economic_market_stabilization", "Market Stabilization", 
                            "Medium cost, medium effectiveness", {"treasury": 20, "noble_support": 15}, 
                            "medium", 0.6, "economic_collapse", "king"),
            PreparationAction("king_economic_currency_devaluation", "Currency Devaluation", 
                            "Low cost, low effectiveness", {"treasury": 10, "noble_support": 10}, 
                            "low", 0.4, "economic_collapse", "king"),
            
            # Supernatural Rift
            PreparationAction("king_supernatural_arcane_research", "Arcane Research", 
                            "High cost, high effectiveness", {"treasury": 30, "noble_support": 20}, 
                            "high", 0.8, "supernatural_rift", "king"),
            PreparationAction("king_supernatural_mystical_defenses", "Mystical Defenses", 
                            "Medium cost, medium effectiveness", {"treasury": 20, "noble_support": 15}, 
                            "medium", 0.6, "supernatural_rift", "king"),
            PreparationAction("king_supernatural_scholar_recruitment", "Scholar Recruitment", 
                            "Low cost, low effectiveness", {"treasury": 10, "noble_support": 10}, 
                            "low", 0.4, "supernatural_rift", "king"),
        ]
    
    def _get_captain_preparation_actions(self) -> List[PreparationAction]:
        """Get Captain preparation actions for all events"""
        return [
            # Famine Cascade
            PreparationAction("captain_famine_food_security", "Food Security Operations", 
                            "High cost, high effectiveness", {"personal_funds": 30, "soldier_count": 20}, 
                            "high", 0.8, "famine_cascade", "captain"),
            PreparationAction("captain_famine_supply_chain", "Supply Chain Protection", 
                            "Medium cost, medium effectiveness", {"personal_funds": 20, "soldier_count": 15}, 
                            "medium", 0.6, "famine_cascade", "captain"),
            PreparationAction("captain_famine_ration_management", "Ration Management", 
                            "Low cost, low effectiveness", {"personal_funds": 10, "soldier_count": 10}, 
                            "low", 0.4, "famine_cascade", "captain"),
            
            # Pandemic Surge
            PreparationAction("captain_pandemic_medical_security", "Medical Security", 
                            "High cost, high effectiveness", {"personal_funds": 30, "health": 20}, 
                            "high", 0.8, "pandemic_surge", "captain"),
            PreparationAction("captain_pandemic_quarantine_enforcement", "Quarantine Enforcement", 
                            "Medium cost, medium effectiveness", {"personal_funds": 20, "health": 15}, 
                            "medium", 0.6, "pandemic_surge", "captain"),
            PreparationAction("captain_pandemic_health_monitoring", "Health Monitoring", 
                            "Low cost, low effectiveness", {"personal_funds": 10, "health": 10}, 
                            "low", 0.4, "pandemic_surge", "captain"),
            
            # Invasion Rebellion
            PreparationAction("captain_invasion_defense_mobilization", "Defense Mobilization", 
                            "High cost, high effectiveness", {"personal_funds": 30, "soldier_count": 20}, 
                            "high", 0.8, "invasion_rebellion", "captain"),
            PreparationAction("captain_invasion_fortress_reinforcement", "Fortress Reinforcement", 
                            "Medium cost, medium effectiveness", {"personal_funds": 20, "soldier_count": 15}, 
                            "medium", 0.6, "invasion_rebellion", "captain"),
            PreparationAction("captain_invasion_patrol_intensification", "Patrol Intensification", 
                            "Low cost, low effectiveness", {"personal_funds": 10, "soldier_count": 10}, 
                            "low", 0.4, "invasion_rebellion", "captain"),
            
            # Cult Uprising
            PreparationAction("captain_cult_infiltration", "Cult Infiltration", 
                            "High cost, high effectiveness", {"personal_funds": 30, "troop_loyalty": 20}, 
                            "high", 0.8, "cult_uprising", "captain"),
            PreparationAction("captain_cult_religious_security", "Religious Security", 
                            "Medium cost, medium effectiveness", {"personal_funds": 20, "troop_loyalty": 15}, 
                            "medium", 0.6, "cult_uprising", "captain"),
            PreparationAction("captain_cult_surveillance_operations", "Surveillance Operations", 
                            "Low cost, low effectiveness", {"personal_funds": 10, "troop_loyalty": 10}, 
                            "low", 0.4, "cult_uprising", "captain"),
            
            # Environmental Catastrophe
            PreparationAction("captain_environmental_disaster_response", "Disaster Response", 
                            "High cost, high effectiveness", {"personal_funds": 30, "soldier_count": 20}, 
                            "high", 0.8, "environmental_catastrophe", "captain"),
            PreparationAction("captain_environmental_evacuation_security", "Evacuation Security", 
                            "Medium cost, medium effectiveness", {"personal_funds": 20, "soldier_count": 15}, 
                            "medium", 0.6, "environmental_catastrophe", "captain"),
            PreparationAction("captain_environmental_emergency_protocols", "Emergency Protocols", 
                            "Low cost, low effectiveness", {"personal_funds": 10, "soldier_count": 10}, 
                            "low", 0.4, "environmental_catastrophe", "captain"),
            
            # Crop Blight
            PreparationAction("captain_crop_agricultural_security", "Agricultural Security", 
                            "High cost, high effectiveness", {"personal_funds": 30, "soldier_count": 20}, 
                            "high", 0.8, "crop_blight", "captain"),
            PreparationAction("captain_crop_farm_protection", "Farm Protection", 
                            "Medium cost, medium effectiveness", {"personal_funds": 20, "soldier_count": 15}, 
                            "medium", 0.6, "crop_blight", "captain"),
            PreparationAction("captain_crop_harvest_security", "Harvest Security", 
                            "Low cost, low effectiveness", {"personal_funds": 10, "soldier_count": 10}, 
                            "low", 0.4, "crop_blight", "captain"),
            
            # Economic Collapse
            PreparationAction("captain_economic_security", "Economic Security", 
                            "High cost, high effectiveness", {"personal_funds": 30, "troop_loyalty": 20}, 
                            "high", 0.8, "economic_collapse", "captain"),
            PreparationAction("captain_economic_market_protection", "Market Protection", 
                            "Medium cost, medium effectiveness", {"personal_funds": 20, "troop_loyalty": 15}, 
                            "medium", 0.6, "economic_collapse", "captain"),
            PreparationAction("captain_economic_trade_security", "Trade Security", 
                            "Low cost, low effectiveness", {"personal_funds": 10, "troop_loyalty": 10}, 
                            "low", 0.4, "economic_collapse", "captain"),
            
            # Supernatural Rift
            PreparationAction("captain_supernatural_arcane_defense", "Arcane Defense", 
                            "High cost, high effectiveness", {"personal_funds": 30, "troop_loyalty": 20}, 
                            "high", 0.8, "supernatural_rift", "captain"),
            PreparationAction("captain_supernatural_mystical_security", "Mystical Security", 
                            "Medium cost, medium effectiveness", {"personal_funds": 20, "troop_loyalty": 15}, 
                            "medium", 0.6, "supernatural_rift", "captain"),
            PreparationAction("captain_supernatural_monitoring", "Supernatural Monitoring", 
                            "Low cost, low effectiveness", {"personal_funds": 10, "troop_loyalty": 10}, 
                            "low", 0.4, "supernatural_rift", "captain"),
        ]
    
    def _get_spy_preparation_actions(self) -> List[PreparationAction]:
        """Get Spy preparation actions for all events"""
        return [
            # Famine Cascade
            PreparationAction("spy_famine_sabotage_prevention", "Food Sabotage Prevention", 
                            "High cost, high effectiveness", {"covert_funds": 30, "cover_identity": 20}, 
                            "high", 0.8, "famine_cascade", "spy"),
            PreparationAction("spy_famine_supply_chain_intelligence", "Supply Chain Intelligence", 
                            "Medium cost, medium effectiveness", {"covert_funds": 20, "cover_identity": 15}, 
                            "medium", 0.6, "famine_cascade", "spy"),
            PreparationAction("spy_famine_agricultural_espionage", "Agricultural Espionage", 
                            "Low cost, low effectiveness", {"covert_funds": 10, "cover_identity": 10}, 
                            "low", 0.4, "famine_cascade", "spy"),
            
            # Pandemic Surge
            PreparationAction("spy_pandemic_biological_warfare_defense", "Biological Warfare Defense", 
                            "High cost, high effectiveness", {"covert_funds": 30, "intelligence": 20}, 
                            "high", 0.8, "pandemic_surge", "spy"),
            PreparationAction("spy_pandemic_medical_intelligence", "Medical Intelligence", 
                            "Medium cost, medium effectiveness", {"covert_funds": 20, "intelligence": 15}, 
                            "medium", 0.6, "pandemic_surge", "spy"),
            PreparationAction("spy_pandemic_health_surveillance", "Health Surveillance", 
                            "Low cost, low effectiveness", {"covert_funds": 10, "intelligence": 10}, 
                            "low", 0.4, "pandemic_surge", "spy"),
            
            # Invasion Rebellion
            PreparationAction("spy_invasion_enemy_infiltration", "Enemy Infiltration", 
                            "High cost, high effectiveness", {"covert_funds": 30, "network_contacts": 20}, 
                            "high", 0.8, "invasion_rebellion", "spy"),
            PreparationAction("spy_invasion_military_intelligence", "Military Intelligence", 
                            "Medium cost, medium effectiveness", {"covert_funds": 20, "network_contacts": 15}, 
                            "medium", 0.6, "invasion_rebellion", "spy"),
            PreparationAction("spy_invasion_threat_assessment", "Threat Assessment", 
                            "Low cost, low effectiveness", {"covert_funds": 10, "network_contacts": 10}, 
                            "low", 0.4, "invasion_rebellion", "spy"),
            
            # Cult Uprising
            PreparationAction("spy_cult_infiltration", "Cult Infiltration", 
                            "High cost, high effectiveness", {"covert_funds": 30, "cover_identity": 20}, 
                            "high", 0.8, "cult_uprising", "spy"),
            PreparationAction("spy_cult_religious_intelligence", "Religious Intelligence", 
                            "Medium cost, medium effectiveness", {"covert_funds": 20, "cover_identity": 15}, 
                            "medium", 0.6, "cult_uprising", "spy"),
            PreparationAction("spy_cult_supernatural_investigation", "Supernatural Investigation", 
                            "Low cost, low effectiveness", {"covert_funds": 10, "cover_identity": 10}, 
                            "low", 0.4, "cult_uprising", "spy"),
            
            # Environmental Catastrophe
            PreparationAction("spy_environmental_disaster_intelligence", "Disaster Intelligence", 
                            "High cost, high effectiveness", {"covert_funds": 30, "intelligence": 20}, 
                            "high", 0.8, "environmental_catastrophe", "spy"),
            PreparationAction("spy_environmental_espionage", "Environmental Espionage", 
                            "Medium cost, medium effectiveness", {"covert_funds": 20, "intelligence": 15}, 
                            "medium", 0.6, "environmental_catastrophe", "spy"),
            PreparationAction("spy_environmental_crisis_monitoring", "Crisis Monitoring", 
                            "Low cost, low effectiveness", {"covert_funds": 10, "intelligence": 10}, 
                            "low", 0.4, "environmental_catastrophe", "spy"),
            
            # Crop Blight
            PreparationAction("spy_crop_agricultural_sabotage_prevention", "Agricultural Sabotage Prevention", 
                            "High cost, high effectiveness", {"covert_funds": 30, "cover_identity": 20}, 
                            "high", 0.8, "crop_blight", "spy"),
            PreparationAction("spy_crop_farm_intelligence", "Farm Intelligence", 
                            "Medium cost, medium effectiveness", {"covert_funds": 20, "cover_identity": 15}, 
                            "medium", 0.6, "crop_blight", "spy"),
            PreparationAction("spy_crop_surveillance", "Crop Surveillance", 
                            "Low cost, low effectiveness", {"covert_funds": 10, "cover_identity": 10}, 
                            "low", 0.4, "crop_blight", "spy"),
            
            # Economic Collapse
            PreparationAction("spy_economic_sabotage_prevention", "Economic Sabotage Prevention", 
                            "High cost, high effectiveness", {"covert_funds": 30, "network_contacts": 20}, 
                            "high", 0.8, "economic_collapse", "spy"),
            PreparationAction("spy_economic_financial_intelligence", "Financial Intelligence", 
                            "Medium cost, medium effectiveness", {"covert_funds": 20, "network_contacts": 15}, 
                            "medium", 0.6, "economic_collapse", "spy"),
            PreparationAction("spy_economic_market_surveillance", "Market Surveillance", 
                            "Low cost, low effectiveness", {"covert_funds": 10, "network_contacts": 10}, 
                            "low", 0.4, "economic_collapse", "spy"),
            
            # Supernatural Rift
            PreparationAction("spy_supernatural_arcane_intelligence", "Arcane Intelligence", 
                            "High cost, high effectiveness", {"covert_funds": 30, "intelligence": 20}, 
                            "high", 0.8, "supernatural_rift", "spy"),
            PreparationAction("spy_supernatural_mystical_espionage", "Mystical Espionage", 
                            "Medium cost, medium effectiveness", {"covert_funds": 20, "intelligence": 15}, 
                            "medium", 0.6, "supernatural_rift", "spy"),
            PreparationAction("spy_supernatural_surveillance", "Supernatural Surveillance", 
                            "Low cost, low effectiveness", {"covert_funds": 10, "intelligence": 10}, 
                            "low", 0.4, "supernatural_rift", "spy"),
        ]
    
    def get_preparation_actions_for_role_and_event(self, role: str, event_id: str) -> List[PreparationAction]:
        """Get preparation actions for specific role and event"""
        role_actions = self.preparation_actions.get(role, [])
        return [action for action in role_actions if action.event_id == event_id]
    
    def can_perform_preparation_action(self, role: str, action_id: str, resources: RoleResources) -> bool:
        """Check if player can perform preparation action"""
        action = self._find_preparation_action(role, action_id)
        if not action:
            return False
        
        role_resources = resources.get_resources_for_role(role)
        
        for resource_name, cost in action.resource_cost.items():
            if role_resources.get(resource_name, 0) < cost:
                return False
        
        return True
    
    def perform_preparation_action(self, role: str, action_id: str, resources: RoleResources) -> PreparationResult:
        """Perform preparation action and calculate effectiveness"""
        action = self._find_preparation_action(role, action_id)
        if not action:
            return PreparationResult(
                success=False,
                effectiveness=0.0,
                resource_cost={},
                message="Preparation action not found",
                threshold_met=False
            )
        
        # Check if player can afford the action
        if not self.can_perform_preparation_action(role, action_id, resources):
            return PreparationResult(
                success=False,
                effectiveness=0.0,
                resource_cost=action.resource_cost,
                message="Insufficient resources for preparation action",
                threshold_met=False
            )
        
        # Calculate effectiveness based on resource investment
        effectiveness = self._calculate_effectiveness(action, resources)
        
        # Check if threshold is met
        threshold_met = self._check_threshold_met(action.event_id, action.effectiveness_level, effectiveness)
        
        return PreparationResult(
            success=True,
            effectiveness=effectiveness,
            resource_cost=action.resource_cost,
            message=f"Preparation action '{action.name}' completed with {int(effectiveness * 100)}% effectiveness",
            threshold_met=threshold_met
        )
    
    def _find_preparation_action(self, role: str, action_id: str) -> Optional[PreparationAction]:
        """Find preparation action by role and action ID"""
        role_actions = self.preparation_actions.get(role, [])
        for action in role_actions:
            if action.action_id == action_id:
                return action
        return None
    
    def _calculate_effectiveness(self, action: PreparationAction, resources: RoleResources) -> float:
        """Calculate preparation effectiveness based on resource investment"""
        role_resources = resources.get_resources_for_role(action.role)
        
        # Base effectiveness from action
        base_effectiveness = action.base_effectiveness
        
        # Resource investment bonus
        total_investment = sum(action.resource_cost.values())
        resource_bonus = min(0.2, total_investment / 100.0)  # Max 20% bonus
        
        # Resource availability penalty
        resource_penalty = 0.0
        for resource_name, cost in action.resource_cost.items():
            available = role_resources.get(resource_name, 0)
            if available < cost * 1.5:  # Need 50% more than cost for full effectiveness
                resource_penalty += 0.1
        
        # Final effectiveness
        final_effectiveness = base_effectiveness + resource_bonus - resource_penalty
        return max(0.0, min(1.0, final_effectiveness))
    
    def _check_threshold_met(self, event_id: str, effectiveness_level: str, effectiveness: float) -> bool:
        """Check if preparation threshold is met"""
        threshold_map = {
            "famine_cascade": {
                "high": self.thresholds.famine_food_reserves_threshold,
                "medium": self.thresholds.famine_agricultural_investment_threshold,
                "low": self.thresholds.famine_trade_embargo_threshold
            },
            "pandemic_surge": {
                "high": self.thresholds.pandemic_medical_infrastructure_threshold,
                "medium": self.thresholds.pandemic_quarantine_protocols_threshold,
                "low": self.thresholds.pandemic_healer_recruitment_threshold
            },
            "invasion_rebellion": {
                "high": self.thresholds.invasion_military_funding_threshold,
                "medium": self.thresholds.invasion_defense_fortification_threshold,
                "low": self.thresholds.invasion_diplomatic_outreach_threshold
            },
            "cult_uprising": {
                "high": self.thresholds.cult_religious_reforms_threshold,
                "medium": self.thresholds.cult_investigation_threshold,
                "low": self.thresholds.cult_public_education_threshold
            },
            "environmental_catastrophe": {
                "high": self.thresholds.environmental_disaster_preparedness_threshold,
                "medium": self.thresholds.environmental_evacuation_plans_threshold,
                "low": self.thresholds.environmental_resource_stockpiling_threshold
            },
            "crop_blight": {
                "high": self.thresholds.crop_seed_distribution_threshold,
                "medium": self.thresholds.crop_agricultural_research_threshold,
                "low": self.thresholds.crop_farmer_support_threshold
            },
            "economic_collapse": {
                "high": self.thresholds.economic_reforms_threshold,
                "medium": self.thresholds.economic_market_stabilization_threshold,
                "low": self.thresholds.economic_currency_devaluation_threshold
            },
            "supernatural_rift": {
                "high": self.thresholds.supernatural_arcane_research_threshold,
                "medium": self.thresholds.supernatural_mystical_defenses_threshold,
                "low": self.thresholds.supernatural_scholar_recruitment_threshold
            }
        }
        
        event_thresholds = threshold_map.get(event_id, {})
        threshold = event_thresholds.get(effectiveness_level, 100)
        
        # Convert effectiveness to resource equivalent (0-1 to 0-100)
        effectiveness_resource = effectiveness * 100
        
        return effectiveness_resource >= threshold
    
    def calculate_crisis_resolution(self, event_id: str, preparation_progress: PreparationProgress) -> Dict[str, Any]:
        """Calculate crisis resolution based on preparation effectiveness"""
        total_effectiveness = preparation_progress.get_total_effectiveness()
        
        if total_effectiveness >= self.game_config.high_effectiveness_threshold:
            outcome = "kingdom_saved"
            message = f"The kingdom faces {event_id}, but your preparations prove highly effective. The crisis is resolved with minimal damage."
        elif total_effectiveness >= self.game_config.medium_effectiveness_threshold:
            outcome = "partial_recovery"
            message = f"The kingdom faces {event_id}, and your preparations help but are not sufficient. The kingdom survives but is weakened."
        else:
            outcome = "kingdom_falls"
            message = f"The kingdom faces {event_id}, but your preparations prove insufficient. The kingdom falls to the crisis."
        
        return {
            "outcome": outcome,
            "effectiveness": total_effectiveness,
            "message": message,
            "preparation_actions": len(preparation_progress.preparation_actions)
        }
