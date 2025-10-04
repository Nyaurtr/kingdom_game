"""
Investigation system implementation for Kingdom Game Version 3.0
Handles evidence gathering with priority-based pools and role-specific access
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
import random
import json
import os
from .game_state import Evidence, TrustLevel
from .game_config import GAME_CONFIG

class EvidenceType(Enum):
    """Types of evidence sources"""
    RUMOR = "rumor"
    OFFICIAL = "official"
    PHYSICAL = "physical"
    LABORATORY = "laboratory"
    INTERCEPTED = "intercepted"
    MARKET = "market"
    PROPHETIC = "prophetic"

class ReliabilityLevel(Enum):
    """Evidence reliability levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class EvidencePool:
    """Evidence pool for a specific event and priority level"""
    event_id: str
    priority_level: str  # "low", "medium", "high"
    evidence_items: List[Dict[str, Any]]
    used_evidence: Set[str] = field(default_factory=set)
    
    def get_available_evidence(self) -> List[Dict[str, Any]]:
        """Get evidence items that haven't been used yet"""
        return [item for item in self.evidence_items if item["id"] not in self.used_evidence]
    
    def select_evidence(self, count: int = 1) -> List[Dict[str, Any]]:
        """Select evidence items using weighted random selection"""
        available = self.get_available_evidence()
        if not available:
            return []
        
        # Weighted selection based on priority level
        weights = {
            "low": 0.3,
            "medium": 0.5, 
            "high": 0.8
        }
        
        weight = weights.get(self.priority_level, 0.5)
        selected = random.choices(available, k=min(count, len(available)))
        
        # Mark as used
        for item in selected:
            self.used_evidence.add(item["id"])
        
        return selected

@dataclass
class InvestigationResult:
    """Result of an investigation action"""
    success: bool
    evidence: Optional[Evidence] = None
    message: str = ""
    resource_cost: Dict[str, int] = field(default_factory=dict)

@dataclass
class CaseboardConnection:
    """Connection between evidence pieces on caseboard"""
    evidence_id_1: str
    evidence_id_2: str
    connection_type: str  # "direct", "suspected", "contradiction", "unclear"
    connection_strength: float = 1.0
    narrative_description: str = ""

class InvestigationSystem:
    """Manages investigation mechanics and evidence gathering with priority-based pools"""
    
    def __init__(self):
        self.evidence_pools: Dict[str, Dict[str, EvidencePool]] = {}
        self.caseboard_patterns = self._initialize_caseboard_patterns()
        self._load_evidence_pools()
    
    def _load_evidence_pools(self):
        """Load evidence pools from JSON files"""
        import sys
        
        # Try to find evidence_pools directory
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(__file__)
        
        evidence_dir = os.path.join(base_path, "src", "core", "evidence_pools")
        
        # If not found, try alternative paths
        if not os.path.exists(evidence_dir):
            evidence_dir = os.path.join(base_path, "evidence_pools")
        
        if not os.path.exists(evidence_dir):
            # Fallback: use embedded data
            self._load_embedded_evidence_pools()
            return
        
        try:
            for filename in os.listdir(evidence_dir):
                if filename.endswith('.json'):
                    event_id = filename.replace('.json', '')
                    filepath = os.path.join(evidence_dir, filename)
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    self.evidence_pools[event_id] = {}
                    
                    for priority_level, evidence_items in data.items():
                        if priority_level in ["low_priority", "medium_priority", "high_priority"]:
                            priority = priority_level.replace("_priority", "")
                            self.evidence_pools[event_id][priority] = EvidencePool(
                                event_id=event_id,
                                priority_level=priority,
                                evidence_items=evidence_items
                            )
        except Exception as e:
            print(f"Error loading evidence pools: {e}")
            # Fallback to embedded data
            self._load_embedded_evidence_pools()
    
    def _load_embedded_evidence_pools(self):
        """Load evidence pools from embedded data"""
        # Embedded evidence data for PyInstaller compatibility
        embedded_evidence = {
            "famine_cascade": {
                "low_priority": [
                    {"content": "Farmers report unusual weather patterns", "reliability": "low", "source_type": "rumor", "location": "Rural Areas"},
                    {"content": "Grain prices have been fluctuating", "reliability": "medium", "source_type": "market_data", "location": "Market District"},
                    {"content": "Some crops are showing signs of disease", "reliability": "medium", "source_type": "observation", "location": "Farmlands"},
                    {"content": "Merchants are hoarding grain supplies", "reliability": "low", "source_type": "rumor", "location": "Trade Quarter"},
                    {"content": "Weather has been unpredictable this season", "reliability": "high", "source_type": "weather_report", "location": "Observatory"}
                ],
                "medium_priority": [
                    {"content": "Agricultural yields are down 30% this season", "reliability": "high", "source_type": "official_report", "location": "Agricultural Ministry"},
                    {"content": "Several farms have reported complete crop failure", "reliability": "high", "source_type": "farmer_testimony", "location": "Northern Farmlands"},
                    {"content": "Grain reserves are at critical levels", "reliability": "high", "source_type": "treasury_report", "location": "Royal Treasury"},
                    {"content": "Food prices have doubled in the past month", "reliability": "high", "source_type": "market_data", "location": "Market District"},
                    {"content": "Merchants are refusing to sell grain", "reliability": "medium", "source_type": "merchant_report", "location": "Trade Quarter"}
                ],
                "high_priority": [
                    {"content": "Kingdom faces imminent famine crisis", "reliability": "high", "source_type": "royal_decree", "location": "Royal Palace"},
                    {"content": "Food reserves will last only 2 weeks", "reliability": "high", "source_type": "emergency_report", "location": "Emergency Council"},
                    {"content": "Mass starvation expected within 3 weeks", "reliability": "high", "source_type": "medical_report", "location": "Royal Infirmary"},
                    {"content": "Agricultural infrastructure has collapsed", "reliability": "high", "source_type": "infrastructure_report", "location": "Public Works"},
                    {"content": "Emergency food distribution has begun", "reliability": "high", "source_type": "emergency_order", "location": "Emergency Council"}
                ]
            },
            "pandemic_surge": {
                "low_priority": [
                    {"content": "People are coughing more than usual", "reliability": "low", "source_type": "observation", "location": "Market District"},
                    {"content": "Healers are seeing more patients", "reliability": "medium", "source_type": "healer_report", "location": "Healer's Guild"},
                    {"content": "Some people have been avoiding crowds", "reliability": "low", "source_type": "observation", "location": "Public Squares"},
                    {"content": "Herbs for treating illness are in high demand", "reliability": "medium", "source_type": "merchant_report", "location": "Herb Market"},
                    {"content": "Rumors of a mysterious illness spreading", "reliability": "low", "source_type": "rumor", "location": "Taverns"}
                ],
                "medium_priority": [
                    {"content": "Disease cases have increased 200% this month", "reliability": "high", "source_type": "medical_report", "location": "Royal Infirmary"},
                    {"content": "Healers report unfamiliar symptoms", "reliability": "high", "source_type": "healer_testimony", "location": "Healer's Guild"},
                    {"content": "Several districts have been quarantined", "reliability": "high", "source_type": "official_order", "location": "City Guard"},
                    {"content": "Medical supplies are running low", "reliability": "high", "source_type": "supply_report", "location": "Medical Supply"},
                    {"content": "People are dying from unknown causes", "reliability": "high", "source_type": "death_records", "location": "City Records"}
                ],
                "high_priority": [
                    {"content": "Pandemic declared by royal decree", "reliability": "high", "source_type": "royal_decree", "location": "Royal Palace"},
                    {"content": "Disease is spreading uncontrollably", "reliability": "high", "source_type": "emergency_report", "location": "Emergency Council"},
                    {"content": "Medical infrastructure has collapsed", "reliability": "high", "source_type": "infrastructure_report", "location": "Public Health"},
                    {"content": "Mass casualties expected within days", "reliability": "high", "source_type": "medical_projection", "location": "Royal Infirmary"},
                    {"content": "Emergency medical protocols activated", "reliability": "high", "source_type": "emergency_order", "location": "Emergency Council"}
                ]
            },
            "invasion_rebellion": {
                "low_priority": [
                    {"content": "Foreign soldiers spotted near the border", "reliability": "low", "source_type": "rumor", "location": "Border Regions"},
                    {"content": "Merchants report unusual military activity", "reliability": "medium", "source_type": "merchant_report", "location": "Trade Routes"},
                    {"content": "Some citizens are acting suspiciously", "reliability": "low", "source_type": "observation", "location": "City Streets"},
                    {"content": "Military supplies are being stockpiled", "reliability": "medium", "source_type": "observation", "location": "Military Barracks"},
                    {"content": "Rumors of a planned attack", "reliability": "low", "source_type": "rumor", "location": "Taverns"}
                ],
                "medium_priority": [
                    {"content": "Enemy forces have crossed the border", "reliability": "high", "source_type": "military_report", "location": "Military Command"},
                    {"content": "Several towns have been captured", "reliability": "high", "source_type": "official_report", "location": "Regional Government"},
                    {"content": "Military casualties are mounting", "reliability": "high", "source_type": "casualty_report", "location": "Military Hospital"},
                    {"content": "Enemy spies have infiltrated the city", "reliability": "high", "source_type": "intelligence_report", "location": "Intelligence Bureau"},
                    {"content": "Defense preparations are underway", "reliability": "high", "source_type": "military_order", "location": "Military Command"}
                ],
                "high_priority": [
                    {"content": "Kingdom is under direct attack", "reliability": "high", "source_type": "royal_decree", "location": "Royal Palace"},
                    {"content": "Enemy forces are advancing on the capital", "reliability": "high", "source_type": "emergency_report", "location": "Emergency Council"},
                    {"content": "Military defenses have been breached", "reliability": "high", "source_type": "military_report", "location": "Military Command"},
                    {"content": "Mass evacuation has been ordered", "reliability": "high", "source_type": "emergency_order", "location": "Emergency Council"},
                    {"content": "Kingdom faces imminent conquest", "reliability": "high", "source_type": "strategic_assessment", "location": "War Council"}
                ]
            },
            "cult_uprising": {
                "low_priority": [
                    {"content": "Strange symbols appearing on walls", "reliability": "low", "source_type": "observation", "location": "City Streets"},
                    {"content": "People gathering in secret meetings", "reliability": "low", "source_type": "rumor", "location": "Residential Areas"},
                    {"content": "Religious texts being distributed", "reliability": "medium", "source_type": "observation", "location": "Market District"},
                    {"content": "Some citizens are acting strangely", "reliability": "low", "source_type": "observation", "location": "Public Squares"},
                    {"content": "Rumors of a new religious movement", "reliability": "low", "source_type": "rumor", "location": "Taverns"}
                ],
                "medium_priority": [
                    {"content": "Cult members have been identified", "reliability": "high", "source_type": "intelligence_report", "location": "Intelligence Bureau"},
                    {"content": "Religious ceremonies are being disrupted", "reliability": "high", "source_type": "religious_report", "location": "Temple District"},
                    {"content": "Several citizens have disappeared", "reliability": "high", "source_type": "missing_persons", "location": "City Guard"},
                    {"content": "Cult is recruiting new members", "reliability": "high", "source_type": "recruitment_report", "location": "Intelligence Bureau"},
                    {"content": "Religious authorities are concerned", "reliability": "high", "source_type": "religious_authority", "location": "High Temple"}
                ],
                "high_priority": [
                    {"content": "Cult uprising declared by royal decree", "reliability": "high", "source_type": "royal_decree", "location": "Royal Palace"},
                    {"content": "Cult is planning to overthrow the kingdom", "reliability": "high", "source_type": "emergency_report", "location": "Emergency Council"},
                    {"content": "Religious infrastructure has been compromised", "reliability": "high", "source_type": "infrastructure_report", "location": "Religious Affairs"},
                    {"content": "Mass conversion efforts are underway", "reliability": "high", "source_type": "conversion_report", "location": "Intelligence Bureau"},
                    {"content": "Emergency religious protocols activated", "reliability": "high", "source_type": "emergency_order", "location": "Emergency Council"}
                ]
            },
            "environmental_catastrophe": {
                "low_priority": [
                    {"content": "Weather has been unusually severe", "reliability": "medium", "source_type": "weather_report", "location": "Observatory"},
                    {"content": "Animals are behaving strangely", "reliability": "low", "source_type": "observation", "location": "Wilderness Areas"},
                    {"content": "Some areas are experiencing unusual phenomena", "reliability": "low", "source_type": "rumor", "location": "Rural Areas"},
                    {"content": "Natural resources are becoming scarce", "reliability": "medium", "source_type": "resource_report", "location": "Resource Management"},
                    {"content": "Environmental changes are noticeable", "reliability": "medium", "source_type": "observation", "location": "Various Locations"}
                ],
                "medium_priority": [
                    {"content": "Natural disasters are increasing in frequency", "reliability": "high", "source_type": "disaster_report", "location": "Emergency Services"},
                    {"content": "Environmental damage is widespread", "reliability": "high", "source_type": "environmental_report", "location": "Environmental Ministry"},
                    {"content": "Natural resources are depleted", "reliability": "high", "source_type": "resource_assessment", "location": "Resource Management"},
                    {"content": "Ecosystems are collapsing", "reliability": "high", "source_type": "ecological_report", "location": "Environmental Ministry"},
                    {"content": "Environmental crisis is escalating", "reliability": "high", "source_type": "crisis_report", "location": "Emergency Services"}
                ],
                "high_priority": [
                    {"content": "Environmental catastrophe declared", "reliability": "high", "source_type": "royal_decree", "location": "Royal Palace"},
                    {"content": "Kingdom faces environmental collapse", "reliability": "high", "source_type": "emergency_report", "location": "Emergency Council"},
                    {"content": "Natural disasters are unstoppable", "reliability": "high", "source_type": "disaster_assessment", "location": "Emergency Services"},
                    {"content": "Environmental infrastructure has failed", "reliability": "high", "source_type": "infrastructure_report", "location": "Environmental Ministry"},
                    {"content": "Emergency environmental protocols activated", "reliability": "high", "source_type": "emergency_order", "location": "Emergency Council"}
                ]
            },
            "crop_blight": {
                "low_priority": [
                    {"content": "Crops are showing signs of disease", "reliability": "medium", "source_type": "observation", "location": "Farmlands"},
                    {"content": "Farmers are reporting crop problems", "reliability": "medium", "source_type": "farmer_report", "location": "Rural Areas"},
                    {"content": "Agricultural yields are declining", "reliability": "medium", "source_type": "yield_report", "location": "Agricultural Ministry"},
                    {"content": "Some crops have failed completely", "reliability": "medium", "source_type": "crop_failure", "location": "Farmlands"},
                    {"content": "Agricultural experts are concerned", "reliability": "medium", "source_type": "expert_opinion", "location": "Agricultural Ministry"}
                ],
                "medium_priority": [
                    {"content": "Crop blight is spreading rapidly", "reliability": "high", "source_type": "blight_report", "location": "Agricultural Ministry"},
                    {"content": "Agricultural production has collapsed", "reliability": "high", "source_type": "production_report", "location": "Agricultural Ministry"},
                    {"content": "Food supplies are critically low", "reliability": "high", "source_type": "supply_report", "location": "Food Distribution"},
                    {"content": "Agricultural infrastructure is failing", "reliability": "high", "source_type": "infrastructure_report", "location": "Agricultural Ministry"},
                    {"content": "Crop blight is unstoppable", "reliability": "high", "source_type": "blight_assessment", "location": "Agricultural Ministry"}
                ],
                "high_priority": [
                    {"content": "Crop blight crisis declared", "reliability": "high", "source_type": "royal_decree", "location": "Royal Palace"},
                    {"content": "Kingdom faces agricultural collapse", "reliability": "high", "source_type": "emergency_report", "location": "Emergency Council"},
                    {"content": "Food production has ceased", "reliability": "high", "source_type": "production_assessment", "location": "Agricultural Ministry"},
                    {"content": "Agricultural infrastructure has collapsed", "reliability": "high", "source_type": "infrastructure_report", "location": "Agricultural Ministry"},
                    {"content": "Emergency agricultural protocols activated", "reliability": "high", "source_type": "emergency_order", "location": "Emergency Council"}
                ]
            },
            "economic_collapse": {
                "low_priority": [
                    {"content": "Merchants are reporting financial difficulties", "reliability": "medium", "source_type": "merchant_report", "location": "Trade Quarter"},
                    {"content": "Prices are fluctuating wildly", "reliability": "medium", "source_type": "price_report", "location": "Market District"},
                    {"content": "Some businesses are closing", "reliability": "medium", "source_type": "business_report", "location": "Commercial District"},
                    {"content": "Economic activity is slowing", "reliability": "medium", "source_type": "economic_report", "location": "Economic Ministry"},
                    {"content": "Financial institutions are struggling", "reliability": "medium", "source_type": "financial_report", "location": "Banking District"}
                ],
                "medium_priority": [
                    {"content": "Economic crisis is deepening", "reliability": "high", "source_type": "crisis_report", "location": "Economic Ministry"},
                    {"content": "Financial markets have collapsed", "reliability": "high", "source_type": "market_report", "location": "Financial District"},
                    {"content": "Businesses are failing en masse", "reliability": "high", "source_type": "business_assessment", "location": "Commercial District"},
                    {"content": "Economic infrastructure is crumbling", "reliability": "high", "source_type": "infrastructure_report", "location": "Economic Ministry"},
                    {"content": "Financial institutions are insolvent", "reliability": "high", "source_type": "financial_assessment", "location": "Banking District"}
                ],
                "high_priority": [
                    {"content": "Economic collapse declared", "reliability": "high", "source_type": "royal_decree", "location": "Royal Palace"},
                    {"content": "Kingdom faces economic ruin", "reliability": "high", "source_type": "emergency_report", "location": "Emergency Council"},
                    {"content": "Economic system has collapsed", "reliability": "high", "source_type": "economic_assessment", "location": "Economic Ministry"},
                    {"content": "Financial infrastructure has failed", "reliability": "high", "source_type": "infrastructure_report", "location": "Financial District"},
                    {"content": "Emergency economic protocols activated", "reliability": "high", "source_type": "emergency_order", "location": "Emergency Council"}
                ]
            },
            "supernatural_rift": {
                "low_priority": [
                    {"content": "Strange occurrences are being reported", "reliability": "low", "source_type": "rumor", "location": "Various Locations"},
                    {"content": "People are experiencing unusual phenomena", "reliability": "low", "source_type": "observation", "location": "City Streets"},
                    {"content": "Some areas feel different", "reliability": "low", "source_type": "observation", "location": "Various Locations"},
                    {"content": "Rumors of supernatural activity", "reliability": "low", "source_type": "rumor", "location": "Taverns"},
                    {"content": "People are acting strangely", "reliability": "low", "source_type": "observation", "location": "Public Squares"}
                ],
                "medium_priority": [
                    {"content": "Supernatural phenomena are confirmed", "reliability": "high", "source_type": "phenomenon_report", "location": "Research Institute"},
                    {"content": "Reality is becoming unstable", "reliability": "high", "source_type": "reality_report", "location": "Research Institute"},
                    {"content": "Supernatural entities have been sighted", "reliability": "high", "source_type": "entity_report", "location": "Research Institute"},
                    {"content": "Supernatural rift is expanding", "reliability": "high", "source_type": "rift_report", "location": "Research Institute"},
                    {"content": "Supernatural crisis is escalating", "reliability": "high", "source_type": "crisis_report", "location": "Research Institute"}
                ],
                "high_priority": [
                    {"content": "Supernatural rift crisis declared", "reliability": "high", "source_type": "royal_decree", "location": "Royal Palace"},
                    {"content": "Kingdom faces supernatural collapse", "reliability": "high", "source_type": "emergency_report", "location": "Emergency Council"},
                    {"content": "Reality is breaking down", "reliability": "high", "source_type": "reality_assessment", "location": "Research Institute"},
                    {"content": "Supernatural infrastructure has failed", "reliability": "high", "source_type": "infrastructure_report", "location": "Research Institute"},
                    {"content": "Emergency supernatural protocols activated", "reliability": "high", "source_type": "emergency_order", "location": "Emergency Council"}
                ]
            }
        }
        
        # Load embedded evidence
        for event_id, event_data in embedded_evidence.items():
            self.evidence_pools[event_id] = {}
            for priority_level, evidence_items in event_data.items():
                priority = priority_level.replace("_priority", "")
                self.evidence_pools[event_id][priority] = EvidencePool(
                    event_id=event_id,
                    priority_level=priority,
                    evidence_items=evidence_items
                )
    
    def get_evidence_pool(self, event_id: str, priority_level: str) -> Optional[EvidencePool]:
        """Get evidence pool for specific event and priority level"""
        return self.evidence_pools.get(event_id, {}).get(priority_level)
    
    def perform_investigation(self, role: str, method_id: str, event_id: str, day: int, resources: Dict[str, int]) -> InvestigationResult:
        """Perform investigation using role-specific method"""
        # Get investigation method from role system
        from .role_system import RoleSystem
        role_system = RoleSystem()
        method = role_system.get_investigation_method(role_system.get_role_by_id(role), method_id)
        
        if not method:
            return InvestigationResult(
                success=False,
                message=f"Investigation method {method_id} not found for role {role}"
            )
        
        # Check resource cost
        for resource_name, cost in method.cost.items():
            if resources.get(resource_name, 0) < cost:
                return InvestigationResult(
                    success=False,
                    message=f"Insufficient {resource_name} for investigation"
                )
        
        # Determine priority level based on day and method
        priority_level = self._determine_priority_level(day, method)
        
        # Get evidence pool
        evidence_pool = self.get_evidence_pool(event_id, priority_level)
        if not evidence_pool:
            return InvestigationResult(
                success=False,
                message=f"No evidence pool found for {event_id} at {priority_level} priority"
            )
        
        # Select evidence
        selected_evidence = evidence_pool.select_evidence(1)
        if not selected_evidence:
            return InvestigationResult(
                success=False,
                message="No more evidence available at this priority level"
            )
        
        # Create Evidence object
        evidence_data = selected_evidence[0]
        evidence = Evidence(
            id=evidence_data["id"],
            content=evidence_data["content"],
            reliability=evidence_data["reliability"],
            source_type=evidence_data["source_type"],
            source_id=evidence_data["source_id"],
            discovered_day=day,
            location=evidence_data["location"],
            verified=False
        )
        
        return InvestigationResult(
            success=True,
            evidence=evidence,
            message=f"Investigation successful: {method.description}",
            resource_cost=method.cost
        )
    
    def _determine_priority_level(self, day: int, method) -> str:
        """Determine priority level based on day and investigation method"""
        # Early game (days 1-2): mostly low priority
        if day <= 2:
            return "low"
        # Mid game (days 3-4): mix of low and medium
        elif day <= 4:
            return random.choice(["low", "medium"])
        # Late game (days 5-7): mostly medium and high
        else:
            return random.choice(["medium", "high"])
    
    def get_available_investigation_methods(self, role: str) -> List[str]:
        """Get available investigation methods for role"""
        from .role_system import RoleSystem
        role_system = RoleSystem()
        role_enum = role_system.get_role_by_id(role)
        if not role_enum:
            return []
        
        methods = role_system.get_investigation_methods(role_enum)
        return [method.method_id for method in methods]
    
    def can_perform_investigation(self, role: str, method_id: str, resources: Dict[str, int]) -> bool:
        """Check if player can perform investigation"""
        from .role_system import RoleSystem
        role_system = RoleSystem()
        method = role_system.get_investigation_method(role_system.get_role_by_id(role), method_id)
        
        if not method:
            return False
        
        # Check resource cost
        for resource_name, cost in method.cost.items():
            if resources.get(resource_name, 0) < cost:
                return False
        
        return True
    
    def _initialize_caseboard_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for caseboard connections"""
        return {
            "famine_patterns": [
                "Rising prices",
                "Empty grain storage", 
                "Farmer complaints",
                "Trade disruption"
            ],
            "disease_patterns": [
                "Increased cases",
                "Strange symptoms",
                "Healer overload",
                "Water contamination"
            ],
            "conspiracy_patterns": [
                "Contradictory information",
                "Unreliable sources",
                "Fake evidence",
                "Missing witnesses"
            ]
        }
    
    def analyze_caseboard_patterns(self, evidence_list: List[Evidence]) -> Dict[str, float]:
        """Analyze caseboard for crisis patterns"""
        pattern_scores = {}
        
        # Count evidence by type and reliability
        evidence_by_type = {}
        high_reliability_count = 0
        
        for evidence in evidence_list:
            if evidence.source_type not in evidence_by_type:
                evidence_by_type[evidence.source_type] = 0
            evidence_by_type[evidence.source_type] += 1
            
            if evidence.reliability == "high":
                high_reliability_count += 1
        
        # Calculate pattern scores based on evidence distribution
        total_evidence = len(evidence_list)
        
        if total_evidence == 0:
            return pattern_scores
        
        # Famine pattern indicators
        famine_score = 0
        if evidence_by_type.get("market", 0) > 0:
            famine_score += 0.3
        if evidence_by_type.get("official", 0) > 0:
            famine_score += 0.2
        if high_reliability_count / total_evidence > 0.5:
            famine_score += 0.2
        
        pattern_scores["famine_cascade"] = famine_score
        
        # Disease pattern indicators  
        disease_score = 0
        if evidence_by_type.get("laboratory", 0) > 0:
            disease_score += 0.4
        if evidence_by_type.get("physical", 0) > 0:
            disease_score += 0.3
        if evidence_by_type.get("rumor", 0) > 0:
            disease_score += 0.1
        
        pattern_scores["pandemic_surge"] = disease_score
        
        # Conspiracy pattern indicators
        conspiracy_score = 0
        if evidence_by_type.get("intercepted", 0) > 0:
            conspiracy_score += 0.4
        if evidence_by_type.get("official", 0) > 0:
            conspiracy_score += 0.2
        if high_reliability_count / total_evidence > 0.7:
            conspiracy_score += 0.2
        
        pattern_scores["conspiracy"] = conspiracy_score
        
        return pattern_scores
    
    def get_investigation_summary(self, evidence_list: List[Evidence]) -> str:
        """Get summary of current investigation progress"""
        if not evidence_list:
            return "No evidence gathered yet."
        
        total_evidence = len(evidence_list)
        verified_evidence = sum(1 for e in evidence_list if e.verified)
        high_reliability = sum(1 for e in evidence_list if e.reliability == "high")
        
        summary = f"Investigation Progress: {total_evidence} pieces of evidence gathered.\n"
        summary += f"Verified evidence: {verified_evidence}/{total_evidence}\n"
        summary += f"High reliability evidence: {high_reliability}/{total_evidence}\n"
        
        # Add pattern analysis
        patterns = self.analyze_caseboard_patterns(evidence_list)
        if patterns:
            strongest_pattern = max(patterns.items(), key=lambda x: x[1])
            if strongest_pattern[1] > 0.5:
                summary += f"Strongest pattern detected: {strongest_pattern[0]} (confidence: {strongest_pattern[1]:.1%})"
        
        return summary