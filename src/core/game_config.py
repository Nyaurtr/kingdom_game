"""
Game configuration constants for Kingdom Game Version 3.0
All configurable values are centralized here for easy adjustment
"""

from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ResourceTransferConfig:
    """Configuration for resource transfer costs"""
    # Transfer cost ratios (0.9 = 10% loss, 0.95 = 5% loss)
    transfer_cost_ratio: float = 0.9
    
    # Transfer costs per resource type
    treasury_to_food_cost: float = 0.9
    food_to_treasury_cost: float = 0.9
    treasury_to_trust_cost: float = 0.85
    trust_to_treasury_cost: float = 0.85
    treasury_to_noble_cost: float = 0.8
    noble_to_treasury_cost: float = 0.8
    
    # Captain resource transfers
    funds_to_health_cost: float = 0.9
    health_to_funds_cost: float = 0.9
    funds_to_loyalty_cost: float = 0.85
    loyalty_to_funds_cost: float = 0.85
    funds_to_soldiers_cost: float = 0.8
    soldiers_to_funds_cost: float = 0.8
    
    # Spy resource transfers
    cover_to_contacts_cost: float = 0.9
    contacts_to_cover_cost: float = 0.9
    cover_to_funds_cost: float = 0.85
    funds_to_cover_cost: float = 0.85
    cover_to_intelligence_cost: float = 0.8
    intelligence_to_cover_cost: float = 0.8

@dataclass
class PreparationThresholds:
    """Thresholds for preparation effectiveness"""
    # Famine Cascade thresholds
    famine_food_reserves_threshold: int = 200
    famine_agricultural_investment_threshold: int = 150
    famine_trade_embargo_threshold: int = 100
    
    # Pandemic Surge thresholds
    pandemic_medical_infrastructure_threshold: int = 200
    pandemic_quarantine_protocols_threshold: int = 150
    pandemic_healer_recruitment_threshold: int = 100
    
    # Invasion Rebellion thresholds
    invasion_military_funding_threshold: int = 200
    invasion_defense_fortification_threshold: int = 150
    invasion_diplomatic_outreach_threshold: int = 100
    
    # Cult Uprising thresholds
    cult_religious_reforms_threshold: int = 200
    cult_investigation_threshold: int = 150
    cult_public_education_threshold: int = 100
    
    # Environmental Catastrophe thresholds
    environmental_disaster_preparedness_threshold: int = 200
    environmental_evacuation_plans_threshold: int = 150
    environmental_resource_stockpiling_threshold: int = 100
    
    # Crop Blight thresholds
    crop_seed_distribution_threshold: int = 200
    crop_agricultural_research_threshold: int = 150
    crop_farmer_support_threshold: int = 100
    
    # Economic Collapse thresholds
    economic_reforms_threshold: int = 200
    economic_market_stabilization_threshold: int = 150
    economic_currency_devaluation_threshold: int = 100
    
    # Supernatural Rift thresholds
    supernatural_arcane_research_threshold: int = 200
    supernatural_mystical_defenses_threshold: int = 150
    supernatural_scholar_recruitment_threshold: int = 100

@dataclass
class RandomEventConfig:
    """Configuration for random events"""
    # Progressive probability per day (0.0 to 1.0)
    daily_probability: List[float] = None
    
    # Maximum events per game
    max_events_per_game: int = 5
    
    # Minimum events per game
    min_events_per_game: int = 3
    
    def __post_init__(self):
        if self.daily_probability is None:
            self.daily_probability = [0.0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90]

@dataclass
class GameConfig:
    """Main game configuration"""
    # Game timing
    total_days: int = 7
    slots_per_day: int = 3
    total_slots: int = 21
    
    # Resource system
    max_resource_value: int = 100
    min_resource_value: int = 0
    initial_resource_value: int = 50
    
    # Preparation system
    high_effectiveness_threshold: float = 0.8
    medium_effectiveness_threshold: float = 0.5
    low_effectiveness_threshold: float = 0.0
    
    # Evidence system
    low_priority_evidence_per_event: int = 20
    medium_priority_evidence_per_event: int = 15
    high_priority_evidence_per_event: int = 10
    
    # Crisis events
    crisis_events: List[str] = None
    
    def __post_init__(self):
        if self.crisis_events is None:
            self.crisis_events = [
                "famine_cascade",
                "pandemic_surge", 
                "invasion_rebellion",
                "cult_uprising",
                "environmental_catastrophe",
                "crop_blight",
                "economic_collapse",
                "supernatural_rift"
            ]

# Global configuration instance
GAME_CONFIG = GameConfig()
RESOURCE_TRANSFER_CONFIG = ResourceTransferConfig()
PREPARATION_THRESHOLDS = PreparationThresholds()
RANDOM_EVENT_CONFIG = RandomEventConfig()
