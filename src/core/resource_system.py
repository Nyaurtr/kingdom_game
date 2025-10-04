"""
Resource management system for Kingdom Game Version 3.0
Handles resource transfers, costs, and validation
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from .game_config import RESOURCE_TRANSFER_CONFIG, GAME_CONFIG
from .game_state import RoleResources

@dataclass
class ResourceTransferResult:
    """Result of a resource transfer operation"""
    success: bool
    source_amount: int
    target_amount: int
    cost_applied: float
    message: str

class ResourceSystem:
    """Manages resource transfers and costs"""
    
    def __init__(self):
        self.transfer_config = RESOURCE_TRANSFER_CONFIG
        self.game_config = GAME_CONFIG
    
    def can_transfer_resources(self, role: str, source_resource: str, target_resource: str, amount: int, resources: RoleResources) -> bool:
        """Check if resource transfer is possible"""
        role_resources = resources.get_resources_for_role(role)
        
        if source_resource not in role_resources or target_resource not in role_resources:
            return False
        
        if role_resources[source_resource] < amount:
            return False
        
        return True
    
    def transfer_resources(self, role: str, source_resource: str, target_resource: str, amount: int, resources: RoleResources) -> ResourceTransferResult:
        """Transfer resources between two resource types"""
        if not self.can_transfer_resources(role, source_resource, target_resource, amount, resources):
            return ResourceTransferResult(
                success=False,
                source_amount=0,
                target_amount=0,
                cost_applied=0.0,
                message=f"Insufficient {source_resource} for transfer"
            )
        
        # Get transfer cost ratio
        cost_ratio = self._get_transfer_cost_ratio(role, source_resource, target_resource)
        
        # Calculate actual amounts
        source_cost = amount
        target_gain = int(amount * cost_ratio)
        
        # Apply the transfer
        current_source = resources.get_resources_for_role(role)[source_resource]
        current_target = resources.get_resources_for_role(role)[target_resource]
        
        resources.set_resource(role, source_resource, current_source - source_cost)
        resources.set_resource(role, target_resource, current_target + target_gain)
        
        return ResourceTransferResult(
            success=True,
            source_amount=source_cost,
            target_amount=target_gain,
            cost_applied=1.0 - cost_ratio,
            message=f"Transferred {source_cost} {source_resource} to {target_gain} {target_resource} (cost: {int((1.0 - cost_ratio) * 100)}%)"
        )
    
    def _get_transfer_cost_ratio(self, role: str, source_resource: str, target_resource: str) -> float:
        """Get transfer cost ratio for specific resource pair"""
        if role == "king":
            return self._get_king_transfer_cost(source_resource, target_resource)
        elif role == "captain":
            return self._get_captain_transfer_cost(source_resource, target_resource)
        elif role == "spy":
            return self._get_spy_transfer_cost(source_resource, target_resource)
        return 1.0
    
    def _get_king_transfer_cost(self, source: str, target: str) -> float:
        """Get transfer cost for King role"""
        if source == "treasury" and target == "food_reserves":
            return self.transfer_config.treasury_to_food_cost
        elif source == "food_reserves" and target == "treasury":
            return self.transfer_config.food_to_treasury_cost
        elif source == "treasury" and target == "public_trust":
            return self.transfer_config.treasury_to_trust_cost
        elif source == "public_trust" and target == "treasury":
            return self.transfer_config.trust_to_treasury_cost
        elif source == "treasury" and target == "noble_support":
            return self.transfer_config.treasury_to_noble_cost
        elif source == "noble_support" and target == "treasury":
            return self.transfer_config.noble_to_treasury_cost
        return 1.0
    
    def _get_captain_transfer_cost(self, source: str, target: str) -> float:
        """Get transfer cost for Captain role"""
        if source == "personal_funds" and target == "health":
            return self.transfer_config.funds_to_health_cost
        elif source == "health" and target == "personal_funds":
            return self.transfer_config.health_to_funds_cost
        elif source == "personal_funds" and target == "troop_loyalty":
            return self.transfer_config.funds_to_loyalty_cost
        elif source == "troop_loyalty" and target == "personal_funds":
            return self.transfer_config.loyalty_to_funds_cost
        elif source == "personal_funds" and target == "soldier_count":
            return self.transfer_config.funds_to_soldiers_cost
        elif source == "soldier_count" and target == "personal_funds":
            return self.transfer_config.soldiers_to_funds_cost
        return 1.0
    
    def _get_spy_transfer_cost(self, source: str, target: str) -> float:
        """Get transfer cost for Spy role"""
        if source == "cover_identity" and target == "network_contacts":
            return self.transfer_config.cover_to_contacts_cost
        elif source == "network_contacts" and target == "cover_identity":
            return self.transfer_config.contacts_to_cover_cost
        elif source == "cover_identity" and target == "covert_funds":
            return self.transfer_config.cover_to_funds_cost
        elif source == "covert_funds" and target == "cover_identity":
            return self.transfer_config.funds_to_cover_cost
        elif source == "cover_identity" and target == "intelligence":
            return self.transfer_config.cover_to_intelligence_cost
        elif source == "intelligence" and target == "cover_identity":
            return self.transfer_config.intelligence_to_cover_cost
        return 1.0
    
    def _get_role_resources(self, role: str) -> Dict[str, int]:
        """Get resource names for specific role"""
        if role == "king":
            return {
                "treasury": 50,
                "food_reserves": 50,
                "public_trust": 50,
                "noble_support": 50
            }
        elif role == "captain":
            return {
                "personal_funds": 50,
                "health": 50,
                "troop_loyalty": 50,
                "soldier_count": 50
            }
        elif role == "spy":
            return {
                "cover_identity": 50,
                "network_contacts": 50,
                "covert_funds": 50,
                "intelligence": 50
            }
        return {}
    
    def validate_resource_value(self, value: int) -> int:
        """Validate and clamp resource value"""
        return max(self.game_config.min_resource_value, 
                  min(self.game_config.max_resource_value, value))
    
    def get_resource_display_name(self, role: str, resource_name: str) -> str:
        """Get display name for resource"""
        display_names = {
            "king": {
                "treasury": "Treasury",
                "food_reserves": "Food Reserves", 
                "public_trust": "Public Trust",
                "noble_support": "Noble Support"
            },
            "captain": {
                "personal_funds": "Personal Funds",
                "health": "Health",
                "troop_loyalty": "Troop Loyalty",
                "soldier_count": "Soldier Count"
            },
            "spy": {
                "cover_identity": "Cover Identity",
                "network_contacts": "Network Contacts",
                "covert_funds": "Covert Funds",
                "intelligence": "Intelligence"
            }
        }
        
        return display_names.get(role, {}).get(resource_name, resource_name)
    
    def get_resource_description(self, role: str, resource_name: str) -> str:
        """Get description for resource"""
        descriptions = {
            "king": {
                "treasury": "National funds for military, infrastructure, emergency aid",
                "food_reserves": "Kingdom food stockpiles for distribution and trade",
                "public_trust": "Citizen confidence in leadership and policies",
                "noble_support": "Aristocracy backing for political decisions"
            },
            "captain": {
                "personal_funds": "Personal money for bribes, equipment, operations",
                "health": "Physical condition affecting combat readiness",
                "troop_loyalty": "Soldier morale and discipline",
                "soldier_count": "Number of available military personnel"
            },
            "spy": {
                "cover_identity": "Maintaining secret identity and infiltration capability",
                "network_contacts": "Information sources and intelligence network",
                "covert_funds": "Secret money for operations and bribes",
                "intelligence": "Information quality and analysis capability"
            }
        }
        
        return descriptions.get(role, {}).get(resource_name, "Resource description not available")
