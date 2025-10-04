"""
Role system implementation for Kingdom Game Version 3.0
Handles King/Captain/Spy roles with resources, actions, and investigation methods
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import random
from .game_config import GAME_CONFIG

class Role(Enum):
    """Available player roles"""
    KING = "king"
    CAPTAIN = "captain" 
    SPY = "spy"

@dataclass
class PersonalSecret:
    """Personal secret for each role"""
    secret_id: str
    name: str
    description: str
    resolution_options: List[str]
    impact_on_ending: Dict[str, str]  # ending_category -> effect_description

@dataclass
class ResourceAcquisitionAction:
    """Resource acquisition action for each role"""
    action_id: str
    name: str
    description: str
    resource_gain: Dict[str, int]
    resource_cost: Dict[str, int]
    effectiveness: float  # 0.0 to 1.0

@dataclass
class InvestigationMethod:
    """Investigation method for each role"""
    method_id: str
    name: str
    description: str
    evidence_access: List[str]  # "low", "medium", "high"
    reliability_bonus: float  # 0.0 to 1.0
    cost: Dict[str, int]  # Resource cost for investigation

@dataclass
class SignatureAction:
    """Signature action for each role"""
    action_id: str
    name: str
    description: str
    success_effects: List[str]
    cost_effects: List[str]
    unlock_conditions: List[str]

@dataclass
class RoleData:
    """Complete role definition"""
    role_id: Role
    name: str
    description: str
    personal_secret: PersonalSecret
    signature_action: SignatureAction
    resource_acquisition_actions: List[ResourceAcquisitionAction]
    investigation_methods: List[InvestigationMethod]
    exclusive_actions: List[str]
    exclusive_npcs: List[str]
    exclusive_set_pieces: List[str]
    ending_variants: List[str]

class RoleSystem:
    """Manages role selection and role-specific mechanics"""
    
    def __init__(self):
        self.roles = self._initialize_roles()
    
    def _initialize_roles(self) -> Dict[Role, RoleData]:
        """Initialize all role data from GDD 3.0"""
        return {
            Role.KING: RoleData(
                role_id=Role.KING,
                name="King",
                description="Supreme ruler, but dreams warn that prestige is declining",
                personal_secret=PersonalSecret(
                    secret_id="blood_debt",
                    name="The Blood Debt",
                    description="King once issued wrong decree, causing innocent family to be slaughtered",
                    resolution_options=["confess", "hide", "investigate", "exploit"],
                    impact_on_ending={
                        "righteous_monarch": "Restore justice for Blood Debt",
                        "tyrant_reformer": "Become tyrant to hide mistakes",
                        "fallen_king": "Overthrown due to wrong decisions",
                        "sacrificial_leader": "Sacrifice self to save kingdom"
                    }
                ),
                signature_action=SignatureAction(
                    action_id="secret_charter",
                    name="Secret Charter",
                    description="Open highest access to raw intelligence",
                    success_effects=["access_all_intelligence", "gain_definitive_evidence"],
                    cost_effects=["treasury_decrease", "advisor_distrust"],
                    unlock_conditions=["complete_day_3", "gain_field_intel"]
                ),
                resource_acquisition_actions=[
                    ResourceAcquisitionAction(
                        action_id="king_tax_collection",
                        name="Tax Collection",
                        description="Increase Treasury, decrease Public Trust",
                        resource_gain={"treasury": 20},
                        resource_cost={"public_trust": 10},
                        effectiveness=0.8
                    ),
                    ResourceAcquisitionAction(
                        action_id="king_trade_negotiations",
                        name="Trade Negotiations",
                        description="Increase Food Reserves, decrease Treasury",
                        resource_gain={"food_reserves": 20},
                        resource_cost={"treasury": 15},
                        effectiveness=0.7
                    ),
                    ResourceAcquisitionAction(
                        action_id="king_resource_redistribution",
                        name="Resource Redistribution",
                        description="Balance resources across categories",
                        resource_gain={"treasury": 10, "food_reserves": 10, "public_trust": 10, "noble_support": 10},
                        resource_cost={},
                        effectiveness=0.6
                    ),
                    ResourceAcquisitionAction(
                        action_id="king_royal_monopolies",
                        name="Royal Monopolies",
                        description="Establish royal monopolies to increase Treasury",
                        resource_gain={"treasury": 25},
                        resource_cost={"public_trust": 15},
                        effectiveness=0.7
                    ),
                    ResourceAcquisitionAction(
                        action_id="king_noble_tributes",
                        name="Noble Tributes",
                        description="Collect tributes from nobles to increase Treasury",
                        resource_gain={"treasury": 20},
                        resource_cost={"noble_support": 10},
                        effectiveness=0.6
                    )
                ],
                investigation_methods=[
                    InvestigationMethod(
                        method_id="king_royal_surveys",
                        name="Royal Surveys",
                        description="Official reports from government officials",
                        evidence_access=["low", "medium"],
                        reliability_bonus=0.3,
                        cost={"treasury": 5}
                    ),
                    InvestigationMethod(
                        method_id="king_noble_consultations",
                        name="Noble Consultations",
                        description="Information from aristocracy and advisors",
                        evidence_access=["medium", "high"],
                        reliability_bonus=0.4,
                        cost={"noble_support": 5}
                    )
                ],
                exclusive_actions=[
                    "council_hearing", "public_appearance", "royal_audit",
                    "issue_decree", "emergency_powers", "appoint_dismiss_advisor",
                    "promise_reward"
                ],
                exclusive_npcs=[
                    "council_secretary_marina", "head_merchant_donovan", 
                    "high_priest_aldric", "court_master_william", "treasury_keeper_anne"
                ],
                exclusive_set_pieces=[
                    "royal_banquet", "public_address", "throne_room_confrontation"
                ],
                ending_variants=[
                    "righteous_monarch", "tyrant_reformer", "fallen_king", "sacrificial_leader"
                ]
            ),
            
            Role.CAPTAIN: RoleData(
                role_id=Role.CAPTAIN,
                name="Captain",
                description="Experienced officer, but dreams show army may be unprepared",
                personal_secret=PersonalSecret(
                    secret_id="ghost_of_discipline",
                    name="The Ghost of Discipline", 
                    description="Captain once ordered wrongful execution, causing innocent death",
                    resolution_options=["confess", "hide", "atonement", "deny"],
                    impact_on_ending={
                        "iron_discipline": "Save kingdom through strict discipline",
                        "compassionate_leader": "Escape Ghost of Discipline through compassion",
                        "fallen_hero": "Die in battle to save others",
                        "rogue_commander": "Abandon chain of command"
                    }
                ),
                signature_action=SignatureAction(
                    action_id="counterintelligence",
                    name="Counterintelligence",
                    description="Unlock ability to detect deception/false evidence",
                    success_effects=["detect_false_flags", "protect_from_planted_evidence"],
                    cost_effects=["source_distrust", "paranoid_reputation"],
                    unlock_conditions=["complete_day_3", "gain_field_intel"]
                ),
                resource_acquisition_actions=[
                    ResourceAcquisitionAction(
                        action_id="captain_personal_training",
                        name="Personal Training",
                        description="Increase Health, decrease Personal Funds",
                        resource_gain={"health": 20},
                        resource_cost={"personal_funds": 15},
                        effectiveness=0.8
                    ),
                    ResourceAcquisitionAction(
                        action_id="captain_equipment_procurement",
                        name="Equipment Procurement",
                        description="Increase Soldier Count, decrease Personal Funds",
                        resource_gain={"soldier_count": 20},
                        resource_cost={"personal_funds": 15},
                        effectiveness=0.7
                    ),
                    ResourceAcquisitionAction(
                        action_id="captain_troop_recruitment",
                        name="Troop Recruitment",
                        description="Increase Soldier Count, decrease Troop Loyalty",
                        resource_gain={"soldier_count": 20},
                        resource_cost={"troop_loyalty": 10},
                        effectiveness=0.6
                    ),
                    ResourceAcquisitionAction(
                        action_id="captain_military_contracts",
                        name="Military Contracts",
                        description="Secure military contracts to increase Personal Funds",
                        resource_gain={"personal_funds": 25},
                        resource_cost={"troop_loyalty": 15},
                        effectiveness=0.7
                    ),
                    ResourceAcquisitionAction(
                        action_id="captain_mercenary_work",
                        name="Mercenary Work",
                        description="Take on mercenary contracts for additional funds",
                        resource_gain={"personal_funds": 20},
                        resource_cost={"health": 10},
                        effectiveness=0.6
                    )
                ],
                investigation_methods=[
                    InvestigationMethod(
                        method_id="captain_military_intelligence",
                        name="Military Intelligence",
                        description="Security reports and troop observations",
                        evidence_access=["low", "medium"],
                        reliability_bonus=0.3,
                        cost={"personal_funds": 5}
                    ),
                    InvestigationMethod(
                        method_id="captain_security_assessments",
                        name="Security Assessments",
                        description="Threat analysis and vulnerability reports",
                        evidence_access=["medium", "high"],
                        reliability_bonus=0.4,
                        cost={"troop_loyalty": 5}
                    )
                ],
                exclusive_actions=[
                    "field_inspection", "patrol_route_analysis", "secure_scene",
                    "deploy_scouts", "fortify_position", "escort_convoy",
                    "interrogation_soft", "interrogation_harsh"
                ],
                exclusive_npcs=[
                    "sergeant_marcus", "scout_lieutenant_elena", 
                    "prison_warden", "local_commander"
                ],
                exclusive_set_pieces=[
                    "war_council", "soldiers_funeral", "barracks_revolt"
                ],
                ending_variants=[
                    "iron_discipline", "compassionate_leader", "fallen_hero", "rogue_commander"
                ]
            ),
            
            Role.SPY: RoleData(
                role_id=Role.SPY,
                name="Spy",
                description="Foreign agent living undercover, but dreams warn secret may be exposed",
                personal_secret=PersonalSecret(
                    secret_id="double_agent",
                    name="The Double Agent",
                    description="Spy working for two sides - current kingdom and another nation",
                    resolution_options=["confess", "hide", "choose_side", "reject_both"],
                    impact_on_ending={
                        "true_believer": "Save kingdom and abandon national loyalties",
                        "successful_mission": "Complete mission for own government",
                        "exposed_traitor": "Identified and must flee",
                        "enlightened_rogue": "Reject both sides and forge own path"
                    }
                ),
                signature_action=SignatureAction(
                    action_id="escape_artist",
                    name="Escape Artist",
                    description="Ability to escape when caught/compromised",
                    success_effects=["escape_any_situation", "no_resource_loss"],
                    cost_effects=["major_reputation_hit", "authority_distrust"],
                    unlock_conditions=["complete_day_3", "gain_field_intel"]
                ),
                resource_acquisition_actions=[
                    ResourceAcquisitionAction(
                        action_id="spy_cover_maintenance",
                        name="Cover Maintenance",
                        description="Increase Cover Identity, decrease Covert Funds",
                        resource_gain={"cover_identity": 20},
                        resource_cost={"covert_funds": 15},
                        effectiveness=0.8
                    ),
                    ResourceAcquisitionAction(
                        action_id="spy_network_expansion",
                        name="Network Expansion",
                        description="Increase Network Contacts, decrease Covert Funds",
                        resource_gain={"network_contacts": 20},
                        resource_cost={"covert_funds": 15},
                        effectiveness=0.7
                    ),
                    ResourceAcquisitionAction(
                        action_id="spy_intelligence_analysis",
                        name="Intelligence Analysis",
                        description="Increase Intelligence, decrease Network Contacts",
                        resource_gain={"intelligence": 20},
                        resource_cost={"network_contacts": 10},
                        effectiveness=0.6
                    ),
                    ResourceAcquisitionAction(
                        action_id="spy_black_market_deals",
                        name="Black Market Deals",
                        description="Engage in black market activities to increase Covert Funds",
                        resource_gain={"covert_funds": 25},
                        resource_cost={"cover_identity": 15},
                        effectiveness=0.7
                    ),
                    ResourceAcquisitionAction(
                        action_id="spy_information_brokering",
                        name="Information Brokering",
                        description="Sell intelligence to increase Covert Funds",
                        resource_gain={"covert_funds": 20},
                        resource_cost={"intelligence": 10},
                        effectiveness=0.6
                    )
                ],
                investigation_methods=[
                    InvestigationMethod(
                        method_id="spy_covert_infiltration",
                        name="Covert Infiltration",
                        description="Secret information gathering",
                        evidence_access=["medium", "high"],
                        reliability_bonus=0.4,
                        cost={"covert_funds": 5}
                    ),
                    InvestigationMethod(
                        method_id="spy_network_intelligence",
                        name="Network Intelligence",
                        description="Information from spy network",
                        evidence_access=["low", "medium", "high"],
                        reliability_bonus=0.3,
                        cost={"network_contacts": 5}
                    )
                ],
                exclusive_actions=[
                    "infiltration", "eavesdropping", "dead_drop_operations",
                    "intercept_decode", "social_engineering", "asset_extraction",
                    "plant_false_evidence", "counterintelligence"
                ],
                exclusive_npcs=[
                    "local_informant", "counter_agent", "handler_contact", "mystery_contact"
                ],
                exclusive_set_pieces=[
                    "dead_drop_contact", "safe_house_infiltration", "final_extraction"
                ],
                ending_variants=[
                    "true_believer", "successful_mission", "exposed_traitor", "enlightened_rogue"
                ]
            )
        }
    
    def get_random_role(self) -> Role:
        """Get a random role for new game"""
        return random.choice(list(Role))
    
    def get_role_data(self, role: Role) -> RoleData:
        """Get complete data for a specific role"""
        return self.roles[role]
    
    def get_all_roles(self) -> List[Role]:
        """Get list of all available roles"""
        return list(Role)
    
    def get_role_by_id(self, role_id: str) -> Optional[Role]:
        """Get role by string ID"""
        try:
            return Role(role_id)
        except ValueError:
            return None
    
    def can_perform_action(self, role: Role, action_id: str) -> bool:
        """Check if role can perform specific action"""
        role_data = self.get_role_data(role)
        return action_id in role_data.exclusive_actions
    
    def get_role_npcs(self, role: Role) -> List[str]:
        """Get NPCs relevant to specific role"""
        role_data = self.get_role_data(role)
        return role_data.exclusive_npcs
    
    def get_signature_action(self, role: Role) -> SignatureAction:
        """Get signature action for role"""
        role_data = self.get_role_data(role)
        return role_data.signature_action
    
    def get_resource_acquisition_actions(self, role: Role) -> List[ResourceAcquisitionAction]:
        """Get resource acquisition actions for role"""
        role_data = self.get_role_data(role)
        return role_data.resource_acquisition_actions
    
    def get_investigation_methods(self, role: Role) -> List[InvestigationMethod]:
        """Get investigation methods for role"""
        role_data = self.get_role_data(role)
        return role_data.investigation_methods
    
    def get_resource_acquisition_action(self, role: Role, action_id: str) -> Optional[ResourceAcquisitionAction]:
        """Get specific resource acquisition action"""
        actions = self.get_resource_acquisition_actions(role)
        for action in actions:
            if action.action_id == action_id:
                return action
        return None
    
    def get_investigation_method(self, role: Role, method_id: str) -> Optional[InvestigationMethod]:
        """Get specific investigation method"""
        methods = self.get_investigation_methods(role)
        for method in methods:
            if method.method_id == method_id:
                return method
        return None
    
    def can_perform_resource_action(self, role: Role, action_id: str) -> bool:
        """Check if role can perform specific resource acquisition action"""
        return self.get_resource_acquisition_action(role, action_id) is not None
    
    def can_perform_investigation(self, role: Role, method_id: str) -> bool:
        """Check if role can perform specific investigation method"""
        return self.get_investigation_method(role, method_id) is not None