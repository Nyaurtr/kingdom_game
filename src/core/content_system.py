"""
Content system for Kingdom Game Version 3.0
Manages dialogues, random events, endings, and narrative content
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import random
from .game_state import GameState, RoleResources
from .game_config import GAME_CONFIG

@dataclass
class DialogueContent:
    """Dialogue content for specific role and action"""
    role: str
    action_type: str  # "investigation", "resource", "preparation"
    action_id: str
    success_messages: List[str]
    failure_messages: List[str]
    neutral_messages: List[str]

@dataclass
class RandomEventContent:
    """Content for random events"""
    event_id: str
    name: str
    description: str
    effects_description: str
    role_specific_messages: Dict[str, str] = field(default_factory=dict)

@dataclass
class EndingContent:
    """Content for game endings"""
    event_id: str
    outcome: str  # "kingdom_saved", "partial_recovery", "kingdom_falls"
    title: str
    description: str
    role_specific_impact: Dict[str, str] = field(default_factory=dict)

class ContentSystem:
    """Manages all game content including dialogues, events, and endings"""
    
    def __init__(self):
        self.dialogue_content = self._initialize_dialogue_content()
        self.random_event_content = self._initialize_random_event_content()
        self.ending_content = self._initialize_ending_content()
        self.daily_narratives = self._initialize_daily_narratives()
    
    def _initialize_dialogue_content(self) -> Dict[str, DialogueContent]:
        """Initialize dialogue content for all roles and actions"""
        return {
            # King Investigation Dialogues
            "king_royal_surveys_success": DialogueContent(
                role="king",
                action_type="investigation",
                action_id="king_royal_surveys",
                success_messages=[
                    "Your advisors present their reports. The kingdom's condition seems stable, but something feels wrong beneath the surface.",
                    "The royal survey reveals concerning patterns in the northern provinces. Something is disrupting the normal flow of life.",
                    "Your officials report unusual activities across the realm. The usual rhythms of governance seem disturbed."
                ],
                failure_messages=[
                    "Your advisors' reports are incomplete and contradictory. The information gathered is unreliable.",
                    "The royal survey encounters resistance. Officials are reluctant to provide accurate information.",
                    "Your investigation yields little useful information. The reports are vague and unhelpful."
                ],
                neutral_messages=[
                    "Your advisors provide routine reports. Nothing unusual is immediately apparent.",
                    "The royal survey proceeds normally. Standard information is gathered.",
                    "Your officials report typical activities. No immediate concerns are raised."
                ]
            ),
            
            "king_noble_consultations_success": DialogueContent(
                role="king",
                action_type="investigation",
                action_id="king_noble_consultations",
                success_messages=[
                    "The aristocracy gathers in your court. Their whispers suggest they know more than they're willing to say.",
                    "Your noble advisors seem nervous. They speak in hushed tones about threats they cannot name.",
                    "The court is abuzz with rumors. Even your most trusted advisors seem uncertain about the kingdom's future."
                ],
                failure_messages=[
                    "The nobility is uncooperative. They provide little useful information.",
                    "Your noble advisors are evasive. Their responses are deliberately vague.",
                    "The court meeting yields no valuable intelligence. The nobles are keeping secrets."
                ],
                neutral_messages=[
                    "The nobility provides routine updates. Standard court business is discussed.",
                    "Your noble advisors report normally. No immediate concerns are raised.",
                    "The court meeting proceeds as usual. Standard political matters are addressed."
                ]
            ),
            
            # King Resource Acquisition Dialogues
            "king_tax_collection_success": DialogueContent(
                role="king",
                action_type="resource",
                action_id="king_tax_collection",
                success_messages=[
                    "You order increased tax collection to bolster the treasury. The people grumble, but the coffers fill.",
                    "Your tax collectors report resistance in some regions. The treasury grows, but at the cost of public goodwill.",
                    "The tax collection proceeds smoothly. The treasury swells, but you sense growing resentment among the common folk."
                ],
                failure_messages=[
                    "Tax collection faces significant resistance. The treasury gains little from this effort.",
                    "Your tax collectors encounter widespread opposition. The treasury increase is minimal.",
                    "The tax collection effort fails. The treasury remains unchanged."
                ],
                neutral_messages=[
                    "Tax collection proceeds normally. The treasury increases modestly.",
                    "Your tax collectors report standard results. The treasury grows slightly.",
                    "The tax collection effort yields expected results. The treasury increases as planned."
                ]
            ),
            
            "king_trade_negotiations_success": DialogueContent(
                role="king",
                action_type="resource",
                action_id="king_trade_negotiations",
                success_messages=[
                    "You negotiate new trade agreements with neighboring kingdoms. Food reserves increase, but the treasury depletes.",
                    "Trade negotiations prove difficult. You secure some food supplies, but at a higher cost than expected.",
                    "Your trade envoys return with mixed results. Some food reserves are secured, but the treasury suffers."
                ],
                failure_messages=[
                    "Trade negotiations fail completely. No food reserves are gained.",
                    "Your trade envoys return empty-handed. The negotiations were unsuccessful.",
                    "Trade agreements collapse. The treasury is wasted with no benefit."
                ],
                neutral_messages=[
                    "Trade negotiations proceed normally. Food reserves increase modestly.",
                    "Your trade envoys achieve standard results. Food reserves grow as expected.",
                    "Trade agreements are reached. Food reserves increase at normal cost."
                ]
            ),
            
            # King Preparation Dialogues
            "king_famine_emergency_food_success": DialogueContent(
                role="king",
                action_type="preparation",
                action_id="king_famine_emergency_food",
                success_messages=[
                    "You order emergency food distribution across the kingdom. Granaries are opened, and the hungry are fed.",
                    "Your food distribution efforts face challenges. Some regions receive aid, while others remain in need.",
                    "The emergency food distribution proceeds smoothly. The kingdom's food crisis begins to ease."
                ],
                failure_messages=[
                    "Emergency food distribution fails. The kingdom's food crisis worsens.",
                    "Your food distribution efforts are ineffective. The hungry remain unfed.",
                    "The emergency food distribution encounters major obstacles. The crisis deepens."
                ],
                neutral_messages=[
                    "Emergency food distribution proceeds normally. Some aid is provided.",
                    "Your food distribution efforts yield moderate results. Partial aid is delivered.",
                    "The emergency food distribution achieves limited success. Some regions are helped."
                ]
            ),
            
            # Captain Investigation Dialogues
            "captain_military_intelligence_success": DialogueContent(
                role="captain",
                action_type="investigation",
                action_id="captain_military_intelligence",
                success_messages=[
                    "Your scouts report unusual activities in the border regions. Something is stirring beyond the kingdom's borders.",
                    "Military intelligence reveals concerning patterns. Enemy movements suggest preparations for something significant.",
                    "Your intelligence network reports strange activities. The usual patterns of military activity seem disrupted."
                ],
                failure_messages=[
                    "Your scouts return with incomplete information. The intelligence gathered is unreliable.",
                    "Military intelligence encounters obstacles. The information gathered is insufficient.",
                    "Your intelligence network fails to provide useful information. The reports are inconclusive."
                ],
                neutral_messages=[
                    "Your scouts report routine activities. No immediate threats are detected.",
                    "Military intelligence provides standard updates. Normal patterns are observed.",
                    "Your intelligence network reports typical activities. No unusual movements are noted."
                ]
            ),
            
            "captain_security_assessments_success": DialogueContent(
                role="captain",
                action_type="investigation",
                action_id="captain_security_assessments",
                success_messages=[
                    "Your security assessment reveals vulnerabilities. The kingdom's defenses may not be sufficient for the coming threat.",
                    "Security reports indicate growing unrest. The usual peace of the realm seems fragile.",
                    "Your security analysis suggests imminent danger. The kingdom's safety cannot be taken for granted."
                ],
                failure_messages=[
                    "Your security assessment yields little useful information. The analysis is inconclusive.",
                    "Security reports are incomplete. The assessment provides no actionable intelligence.",
                    "Your security analysis fails to identify key threats. The assessment is inadequate."
                ],
                neutral_messages=[
                    "Your security assessment reveals standard vulnerabilities. Normal security measures are adequate.",
                    "Security reports indicate routine concerns. Standard security protocols are sufficient.",
                    "Your security analysis shows normal patterns. No immediate threats are identified."
                ]
            ),
            
            # Captain Resource Acquisition Dialogues
            "captain_personal_training_success": DialogueContent(
                role="captain",
                action_type="resource",
                action_id="captain_personal_training",
                success_messages=[
                    "You spend time training and improving your physical condition. Your health improves, but your personal funds decrease.",
                    "Your training regimen faces challenges. Some improvements are made, but at a higher cost than expected.",
                    "Your personal training succeeds. Your physical condition improves significantly."
                ],
                failure_messages=[
                    "Your training regimen fails to improve your condition. Your health remains unchanged.",
                    "Personal training encounters obstacles. Your physical condition shows no improvement.",
                    "Your training effort is ineffective. Your health does not improve."
                ],
                neutral_messages=[
                    "Your training regimen proceeds normally. Your health improves modestly.",
                    "Personal training yields standard results. Your physical condition improves as expected.",
                    "Your training effort achieves moderate success. Your health improves slightly."
                ]
            ),
            
            "captain_equipment_procurement_success": DialogueContent(
                role="captain",
                action_type="resource",
                action_id="captain_equipment_procurement",
                success_messages=[
                    "You purchase new equipment for your forces. Your soldier count increases, but your personal funds decrease.",
                    "Equipment procurement faces obstacles. Some units are equipped, while others remain under-supplied.",
                    "Your equipment procurement succeeds. Your forces are better equipped for battle."
                ],
                failure_messages=[
                    "Equipment procurement fails completely. No new equipment is acquired.",
                    "Your equipment purchase effort is unsuccessful. Your forces remain under-equipped.",
                    "Equipment procurement encounters major obstacles. No soldiers are gained."
                ],
                neutral_messages=[
                    "Equipment procurement proceeds normally. Your forces are moderately equipped.",
                    "Your equipment purchase yields standard results. Your forces are adequately equipped.",
                    "Equipment procurement achieves expected results. Your forces are properly equipped."
                ]
            ),
            
            # Captain Preparation Dialogues
            "captain_famine_food_security_success": DialogueContent(
                role="captain",
                action_type="preparation",
                action_id="captain_famine_food_security",
                success_messages=[
                    "You deploy your forces to protect food supplies. Military units guard granaries and distribution centers.",
                    "Your food security operations face challenges. Some supplies are protected, while others remain vulnerable.",
                    "The food security operations succeed. The kingdom's food supplies are well-protected."
                ],
                failure_messages=[
                    "Food security operations fail. The kingdom's food supplies remain unprotected.",
                    "Your food security efforts are ineffective. The supplies are vulnerable to attack.",
                    "The food security operations encounter major obstacles. The supplies are at risk."
                ],
                neutral_messages=[
                    "Food security operations proceed normally. Some supplies are protected.",
                    "Your food security efforts yield moderate results. Partial protection is provided.",
                    "The food security operations achieve limited success. Some supplies are secured."
                ]
            ),
            
            # Spy Investigation Dialogues
            "spy_covert_infiltration_success": DialogueContent(
                role="spy",
                action_type="investigation",
                action_id="spy_covert_infiltration",
                success_messages=[
                    "You infiltrate suspicious groups and organizations. Hidden information is revealed through secret channels.",
                    "Your infiltration operations face obstacles. Some groups are penetrated, while others remain impenetrable.",
                    "The covert infiltration succeeds. Valuable intelligence is gathered from hidden sources."
                ],
                failure_messages=[
                    "Your infiltration operations fail. No useful intelligence is gathered.",
                    "Covert infiltration encounters major obstacles. The operation is unsuccessful.",
                    "Your infiltration effort is compromised. No intelligence is gained."
                ],
                neutral_messages=[
                    "Your infiltration operations proceed normally. Some intelligence is gathered.",
                    "Covert infiltration yields moderate results. Partial intelligence is obtained.",
                    "Your infiltration effort achieves limited success. Some information is gathered."
                ]
            ),
            
            "spy_network_intelligence_success": DialogueContent(
                role="spy",
                action_type="investigation",
                action_id="spy_network_intelligence",
                success_messages=[
                    "Your spy network reports unusual activities. Information flows through secret channels, revealing hidden threats.",
                    "Your intelligence network faces challenges. Some sources provide information, while others remain silent.",
                    "The network intelligence gathering succeeds. Valuable information is collected from multiple sources."
                ],
                failure_messages=[
                    "Your spy network fails to provide useful information. The intelligence gathered is unreliable.",
                    "Network intelligence encounters obstacles. The information gathered is insufficient.",
                    "Your intelligence network is compromised. No useful information is obtained."
                ],
                neutral_messages=[
                    "Your spy network provides routine updates. Standard intelligence is gathered.",
                    "Network intelligence yields normal results. Expected information is obtained.",
                    "Your intelligence network reports typical activities. Standard intelligence is collected."
                ]
            ),
            
            # Spy Resource Acquisition Dialogues
            "spy_cover_maintenance_success": DialogueContent(
                role="spy",
                action_type="resource",
                action_id="spy_cover_maintenance",
                success_messages=[
                    "You invest in maintaining your cover identity. Your cover identity improves, but your covert funds decrease.",
                    "Your cover maintenance faces challenges. Some improvements are made, but at a higher cost than expected.",
                    "Your cover maintenance succeeds. Your secret identity is more secure."
                ],
                failure_messages=[
                    "Your cover maintenance fails. Your cover identity remains vulnerable.",
                    "Cover maintenance encounters obstacles. Your secret identity is compromised.",
                    "Your cover maintenance effort is ineffective. Your cover identity shows no improvement."
                ],
                neutral_messages=[
                    "Your cover maintenance proceeds normally. Your cover identity improves modestly.",
                    "Cover maintenance yields standard results. Your secret identity is adequately maintained.",
                    "Your cover maintenance effort achieves expected results. Your cover identity is properly maintained."
                ]
            ),
            
            "spy_network_expansion_success": DialogueContent(
                role="spy",
                action_type="resource",
                action_id="spy_network_expansion",
                success_messages=[
                    "You expand your spy network. Your network contacts increase, but your covert funds decrease.",
                    "Network expansion faces obstacles. Some new contacts are made, while others remain elusive.",
                    "Your network expansion succeeds. Your intelligence network is significantly expanded."
                ],
                failure_messages=[
                    "Network expansion fails completely. No new contacts are made.",
                    "Your network expansion effort is unsuccessful. Your network remains unchanged.",
                    "Network expansion encounters major obstacles. No contacts are gained."
                ],
                neutral_messages=[
                    "Network expansion proceeds normally. Your network grows modestly.",
                    "Your network expansion yields standard results. Your network grows as expected.",
                    "Network expansion achieves expected results. Your network grows properly."
                ]
            ),
            
            # Spy Preparation Dialogues
            "spy_famine_sabotage_prevention_success": DialogueContent(
                role="spy",
                action_type="preparation",
                action_id="spy_famine_sabotage_prevention",
                success_messages=[
                    "You deploy covert operations to prevent food sabotage. Secret agents protect food supplies from hidden threats.",
                    "Your food sabotage prevention faces obstacles. Some supplies are protected, while others remain vulnerable.",
                    "The food sabotage prevention succeeds. The kingdom's food supplies are protected from covert threats."
                ],
                failure_messages=[
                    "Food sabotage prevention fails. The kingdom's food supplies remain vulnerable to covert threats.",
                    "Your food sabotage prevention efforts are ineffective. The supplies are at risk from hidden attacks.",
                    "The food sabotage prevention operations encounter major obstacles. The supplies are unprotected."
                ],
                neutral_messages=[
                    "Food sabotage prevention proceeds normally. Some supplies are protected from covert threats.",
                    "Your food sabotage prevention efforts yield moderate results. Partial protection is provided.",
                    "The food sabotage prevention operations achieve limited success. Some supplies are secured."
                ]
            )
        }
    
    def _initialize_random_event_content(self) -> Dict[str, RandomEventContent]:
        """Initialize random event content"""
        return {
            "heavy_rain": RandomEventContent(
                event_id="heavy_rain",
                name="Heavy Rain",
                description="Heavy rain falls across the kingdom. Visibility is reduced, and military operations are hindered.",
                effects_description="Military effectiveness reduced, investigation accuracy affected",
                role_specific_messages={
                    "king": "The heavy rain disrupts your royal surveys and noble consultations.",
                    "captain": "The downpour affects your military intelligence and security assessments.",
                    "spy": "The rain hampers your covert infiltration and network intelligence operations."
                }
            ),
            "drought": RandomEventContent(
                event_id="drought",
                name="Drought",
                description="A severe drought affects the kingdom. Food production decreases, and famine vulnerability increases.",
                effects_description="Food production reduced, famine vulnerability increased",
                role_specific_messages={
                    "king": "The drought threatens your food reserves and public trust.",
                    "captain": "The drought affects your troop loyalty and soldier count.",
                    "spy": "The drought impacts your network contacts and intelligence gathering."
                }
            ),
            "storm": RandomEventContent(
                event_id="storm",
                name="Storm",
                description="A powerful storm sweeps across the kingdom. Trade routes are disrupted, and economic stability is affected.",
                effects_description="Trade routes disrupted, economic stability affected",
                role_specific_messages={
                    "king": "The storm disrupts your trade negotiations and treasury management.",
                    "captain": "The storm affects your equipment procurement and troop recruitment.",
                    "spy": "The storm impacts your covert funds and network expansion."
                }
            ),
            "fog": RandomEventContent(
                event_id="fog",
                name="Fog",
                description="Thick fog blankets the kingdom. Visibility is reduced, and investigation accuracy is affected.",
                effects_description="Investigation accuracy reduced, visibility decreased",
                role_specific_messages={
                    "king": "The fog hampers your royal surveys and noble consultations.",
                    "captain": "The fog affects your military intelligence and security assessments.",
                    "spy": "The fog impacts your covert infiltration and network intelligence."
                }
            ),
            "noble_conflict": RandomEventContent(
                event_id="noble_conflict",
                name="Noble Conflict",
                description="Noble families are in conflict. Political stability is threatened, and noble support decreases.",
                effects_description="Noble support decreased, political stability threatened",
                role_specific_messages={
                    "king": "The noble conflict threatens your noble support and political stability.",
                    "captain": "The noble conflict affects your troop loyalty and military operations.",
                    "spy": "The noble conflict impacts your network contacts and intelligence gathering."
                }
            ),
            "public_unrest": RandomEventContent(
                event_id="public_unrest",
                name="Public Unrest",
                description="Public unrest spreads across the kingdom. Social stability is threatened, and public trust decreases.",
                effects_description="Public trust decreased, social stability threatened",
                role_specific_messages={
                    "king": "The public unrest threatens your public trust and social stability.",
                    "captain": "The public unrest affects your troop loyalty and security operations.",
                    "spy": "The public unrest impacts your cover identity and network contacts."
                }
            ),
            "market_crash": RandomEventContent(
                event_id="market_crash",
                name="Market Crash",
                description="The market experiences a sudden crash. Economic stability is threatened, and treasury resources decrease.",
                effects_description="Treasury decreased, economic stability threatened",
                role_specific_messages={
                    "king": "The market crash threatens your treasury and economic stability.",
                    "captain": "The market crash affects your personal funds and equipment procurement.",
                    "spy": "The market crash impacts your covert funds and network expansion."
                }
            ),
            "resource_shortage": RandomEventContent(
                event_id="resource_shortage",
                name="Resource Shortage",
                description="A critical resource shortage affects the kingdom. Resource availability decreases, and preparation becomes more difficult.",
                effects_description="Resource availability decreased, preparation difficulty increased",
                role_specific_messages={
                    "king": "The resource shortage threatens your treasury and food reserves.",
                    "captain": "The resource shortage affects your personal funds and health.",
                    "spy": "The resource shortage impacts your covert funds and cover identity."
                }
            ),
            "trade_windfall": RandomEventContent(
                event_id="trade_windfall",
                name="Trade Windfall",
                description="Unexpected trade opportunities arise. Economic stability improves, and treasury resources increase.",
                effects_description="Treasury increased, economic stability improved",
                role_specific_messages={
                    "king": "The trade windfall benefits your treasury and economic stability.",
                    "captain": "The trade windfall benefits your personal funds and equipment procurement.",
                    "spy": "The trade windfall benefits your covert funds and network expansion."
                }
            ),
            "resource_discovery": RandomEventContent(
                event_id="resource_discovery",
                name="Resource Discovery",
                description="New resources are discovered within the kingdom. Resource availability increases, and preparation becomes easier.",
                effects_description="Resource availability increased, preparation difficulty decreased",
                role_specific_messages={
                    "king": "The resource discovery benefits your treasury and food reserves.",
                    "captain": "The resource discovery benefits your personal funds and health.",
                    "spy": "The resource discovery benefits your covert funds and cover identity."
                }
            ),
            "troop_morale_boost": RandomEventContent(
                event_id="troop_morale_boost",
                name="Troop Morale Boost",
                description="Your troops experience a morale boost. Military effectiveness improves, and troop loyalty increases.",
                effects_description="Troop loyalty increased, military effectiveness improved",
                role_specific_messages={
                    "king": "The troop morale boost benefits your noble support and political stability.",
                    "captain": "The troop morale boost benefits your troop loyalty and military effectiveness.",
                    "spy": "The troop morale boost benefits your network contacts and intelligence gathering."
                }
            ),
            "equipment_malfunction": RandomEventContent(
                event_id="equipment_malfunction",
                name="Equipment Malfunction",
                description="Equipment malfunctions affect your forces. Military readiness decreases, and soldier count is reduced.",
                effects_description="Soldier count decreased, military readiness reduced",
                role_specific_messages={
                    "king": "The equipment malfunction threatens your noble support and military readiness.",
                    "captain": "The equipment malfunction threatens your soldier count and military effectiveness.",
                    "spy": "The equipment malfunction impacts your network contacts and intelligence operations."
                }
            ),
            "training_success": RandomEventContent(
                event_id="training_success",
                name="Training Success",
                description="Your training programs succeed beyond expectations. Military effectiveness improves, and health increases.",
                effects_description="Health increased, military effectiveness improved",
                role_specific_messages={
                    "king": "The training success benefits your public trust and social stability.",
                    "captain": "The training success benefits your health and military effectiveness.",
                    "spy": "The training success benefits your cover identity and intelligence operations."
                }
            ),
            "security_breach": RandomEventContent(
                event_id="security_breach",
                name="Security Breach",
                description="A security breach compromises your operations. Covert effectiveness decreases, and cover identity is reduced.",
                effects_description="Cover identity decreased, covert effectiveness reduced",
                role_specific_messages={
                    "king": "The security breach threatens your public trust and political stability.",
                    "captain": "The security breach affects your troop loyalty and security operations.",
                    "spy": "The security breach threatens your cover identity and covert operations."
                }
            )
        }
    
    def _initialize_ending_content(self) -> Dict[str, EndingContent]:
        """Initialize ending content for all events and outcomes"""
        return {
            # Famine Cascade Endings
            "famine_cascade_kingdom_saved": EndingContent(
                event_id="famine_cascade",
                outcome="kingdom_saved",
                title="Kingdom Saved - Famine Averted",
                description="The kingdom faces a devastating famine, but your preparations prove effective. Emergency food distribution saves countless lives, and agricultural investments ensure long-term food security. The kingdom not only survives but emerges stronger, with improved food production and distribution systems.",
                role_specific_impact={
                    "king": "Your royal leadership and resource management saved the kingdom from starvation.",
                    "captain": "Your military protection of food supplies ensured the kingdom's survival.",
                    "spy": "Your covert operations prevented food sabotage and protected the kingdom's supplies."
                }
            ),
            "famine_cascade_partial_recovery": EndingContent(
                event_id="famine_cascade",
                outcome="partial_recovery",
                title="Partial Recovery - Famine Contained",
                description="The kingdom faces a devastating famine, and your preparations help but are not sufficient. Some regions receive aid and survive, while others suffer severe food shortages. The kingdom survives but is weakened, with ongoing food security challenges.",
                role_specific_impact={
                    "king": "Your efforts helped some regions survive, but the kingdom remains vulnerable to future famines.",
                    "captain": "Your military operations protected some supplies, but the kingdom's food security is compromised.",
                    "spy": "Your covert operations prevented some sabotage, but the kingdom's food supplies remain at risk."
                }
            ),
            "famine_cascade_kingdom_falls": EndingContent(
                event_id="famine_cascade",
                outcome="kingdom_falls",
                title="Kingdom Falls - Famine Devastation",
                description="The kingdom faces a devastating famine, and your preparations prove insufficient. Food shortages spread unchecked, and the kingdom collapses under the weight of starvation and social breakdown. The kingdom falls, and its people suffer greatly.",
                role_specific_impact={
                    "king": "Your royal leadership failed to prevent the famine, and the kingdom collapsed.",
                    "captain": "Your military operations were insufficient to protect the kingdom from starvation.",
                    "spy": "Your covert operations failed to prevent the famine, and the kingdom was destroyed."
                }
            ),
            
            # Pandemic Surge Endings
            "pandemic_surge_kingdom_saved": EndingContent(
                event_id="pandemic_surge",
                outcome="kingdom_saved",
                title="Kingdom Saved - Pandemic Contained",
                description="A deadly pandemic threatens the kingdom, but your medical preparations save the day. Quarantine protocols contain the spread, and medical infrastructure treats the afflicted. The kingdom not only survives but emerges healthier, with improved medical systems and disease prevention.",
                role_specific_impact={
                    "king": "Your royal leadership and medical investments saved the kingdom from the pandemic.",
                    "captain": "Your military security operations protected medical facilities and contained the disease.",
                    "spy": "Your covert operations prevented biological warfare and protected the kingdom's health."
                }
            ),
            "pandemic_surge_partial_recovery": EndingContent(
                event_id="pandemic_surge",
                outcome="partial_recovery",
                title="Partial Recovery - Pandemic Controlled",
                description="A deadly pandemic threatens the kingdom, and your medical preparations help but are not sufficient. Some regions are protected and treated, while others suffer severe outbreaks. The kingdom survives but is weakened, with ongoing health challenges.",
                role_specific_impact={
                    "king": "Your efforts helped some regions survive, but the kingdom remains vulnerable to future pandemics.",
                    "captain": "Your military operations protected some facilities, but the kingdom's health security is compromised.",
                    "spy": "Your covert operations prevented some biological attacks, but the kingdom's health remains at risk."
                }
            ),
            "pandemic_surge_kingdom_falls": EndingContent(
                event_id="pandemic_surge",
                outcome="kingdom_falls",
                title="Kingdom Falls - Pandemic Devastation",
                description="A deadly pandemic threatens the kingdom, and your medical preparations prove insufficient. The disease spreads unchecked, and the kingdom collapses under the weight of illness and death. The kingdom falls, and its people suffer greatly.",
                role_specific_impact={
                    "king": "Your royal leadership failed to prevent the pandemic, and the kingdom collapsed.",
                    "captain": "Your military operations were insufficient to protect the kingdom from the disease.",
                    "spy": "Your covert operations failed to prevent the pandemic, and the kingdom was destroyed."
                }
            ),
            
            # Invasion Rebellion Endings
            "invasion_rebellion_kingdom_saved": EndingContent(
                event_id="invasion_rebellion",
                outcome="kingdom_saved",
                title="Kingdom Saved - Invasion Repelled",
                description="Enemy forces threaten the kingdom, but your military preparations prove decisive. Defense fortifications repel the invaders, and diplomatic outreach prevents further conflict. The kingdom not only survives but emerges more secure, with strengthened defenses and improved relations.",
                role_specific_impact={
                    "king": "Your royal leadership and military funding saved the kingdom from invasion.",
                    "captain": "Your military operations and defense preparations repelled the enemy forces.",
                    "spy": "Your covert operations and enemy infiltration prevented the invasion."
                }
            ),
            "invasion_rebellion_partial_recovery": EndingContent(
                event_id="invasion_rebellion",
                outcome="partial_recovery",
                title="Partial Recovery - Invasion Contained",
                description="Enemy forces threaten the kingdom, and your military preparations help but are not sufficient. Some regions are defended and protected, while others fall to the invaders. The kingdom survives but is weakened, with ongoing security challenges.",
                role_specific_impact={
                    "king": "Your efforts helped some regions survive, but the kingdom remains vulnerable to future invasions.",
                    "captain": "Your military operations protected some regions, but the kingdom's security is compromised.",
                    "spy": "Your covert operations prevented some attacks, but the kingdom's security remains at risk."
                }
            ),
            "invasion_rebellion_kingdom_falls": EndingContent(
                event_id="invasion_rebellion",
                outcome="kingdom_falls",
                title="Kingdom Falls - Invasion Success",
                description="Enemy forces threaten the kingdom, and your military preparations prove insufficient. The invaders overwhelm the defenses, and the kingdom falls to foreign occupation or internal rebellion. The kingdom falls, and its people suffer greatly.",
                role_specific_impact={
                    "king": "Your royal leadership failed to prevent the invasion, and the kingdom collapsed.",
                    "captain": "Your military operations were insufficient to protect the kingdom from invasion.",
                    "spy": "Your covert operations failed to prevent the invasion, and the kingdom was destroyed."
                }
            ),
            
            # Cult Uprising Endings
            "cult_uprising_kingdom_saved": EndingContent(
                event_id="cult_uprising",
                outcome="kingdom_saved",
                title="Kingdom Saved - Cult Eliminated",
                description="A dangerous cult threatens the kingdom, but your investigation and preparation efforts expose and eliminate the threat. Cult infiltration reveals their plans, and religious reforms prevent future uprisings. The kingdom not only survives but emerges more united, with improved religious harmony.",
                role_specific_impact={
                    "king": "Your royal leadership and religious reforms eliminated the cult threat.",
                    "captain": "Your military operations and cult infiltration exposed and eliminated the threat.",
                    "spy": "Your covert operations and cult infiltration prevented the uprising."
                }
            ),
            "cult_uprising_partial_recovery": EndingContent(
                event_id="cult_uprising",
                outcome="partial_recovery",
                title="Partial Recovery - Cult Weakened",
                description="A dangerous cult threatens the kingdom, and your investigation and preparation efforts help but are not sufficient. Some cult activities are exposed and stopped, while others continue to threaten the kingdom. The kingdom survives but is weakened, with ongoing religious conflicts.",
                role_specific_impact={
                    "king": "Your efforts helped expose some cult activities, but the kingdom remains vulnerable to future uprisings.",
                    "captain": "Your military operations weakened some cult activities, but the kingdom's religious security is compromised.",
                    "spy": "Your covert operations prevented some cult activities, but the kingdom's religious security remains at risk."
                }
            ),
            "cult_uprising_kingdom_falls": EndingContent(
                event_id="cult_uprising",
                outcome="kingdom_falls",
                title="Kingdom Falls - Cult Dominance",
                description="A dangerous cult threatens the kingdom, and your investigation and preparation efforts prove insufficient. The cult gains power and influence, and the kingdom falls to religious extremism or supernatural corruption. The kingdom falls, and its people suffer greatly.",
                role_specific_impact={
                    "king": "Your royal leadership failed to prevent the cult uprising, and the kingdom collapsed.",
                    "captain": "Your military operations were insufficient to protect the kingdom from the cult.",
                    "spy": "Your covert operations failed to prevent the cult uprising, and the kingdom was destroyed."
                }
            )
        }
    
    def _initialize_daily_narratives(self) -> Dict[str, Dict[str, str]]:
        """Initialize daily narrative content"""
        return {
            "day_1": {
                "king": "You wake from a disturbing dream. Visions of disaster haunt your sleep, warning of catastrophe approaching your kingdom. As the supreme ruler, you must investigate these omens and prepare your realm for whatever threat approaches.",
                "captain": "You wake from a disturbing dream. Visions of disaster haunt your sleep, warning of catastrophe approaching your kingdom. As the military leader, you must investigate these threats and prepare your forces for whatever danger approaches.",
                "spy": "You wake from a disturbing dream. Visions of disaster haunt your sleep, warning of catastrophe approaching your kingdom. As a covert agent, you must investigate these threats and prepare your network for whatever danger approaches."
            },
            "day_2": {
                "king": "The second day brings more clarity to your dreams. The threat seems more tangible now, and you must act quickly to gather information and prepare your kingdom.",
                "captain": "The second day reveals more about the coming threat. Your military instincts tell you that time is running short, and you must gather intelligence and prepare your forces.",
                "spy": "The second day provides more insight into the approaching danger. Your covert instincts tell you that you must gather intelligence and prepare your network for the coming crisis."
            },
            "day_3": {
                "king": "The third day marks a turning point. The threat is becoming clearer, and you must make crucial decisions about how to prepare your kingdom for the coming crisis.",
                "captain": "The third day brings critical intelligence. The threat is taking shape, and you must make important decisions about how to prepare your forces for the coming battle.",
                "spy": "The third day reveals crucial information. The threat is becoming more defined, and you must make key decisions about how to prepare your network for the coming crisis."
            },
            "day_4": {
                "king": "The fourth day brings urgency. The threat is now clear, and you must intensify your preparations to save your kingdom from the coming crisis.",
                "captain": "The fourth day demands action. The threat is now evident, and you must intensify your military preparations to protect your kingdom from the coming danger.",
                "spy": "The fourth day requires decisive action. The threat is now apparent, and you must intensify your covert operations to protect your kingdom from the coming crisis."
            },
            "day_5": {
                "king": "The fifth day brings desperation. The crisis is approaching rapidly, and you must make final preparations to save your kingdom from destruction.",
                "captain": "The fifth day demands immediate action. The crisis is approaching fast, and you must make final military preparations to protect your kingdom from destruction.",
                "spy": "The fifth day requires urgent action. The crisis is approaching quickly, and you must make final covert preparations to protect your kingdom from destruction."
            },
            "day_6": {
                "king": "The sixth day brings final urgency. The crisis is upon you, and you must make your last preparations to save your kingdom from the coming destruction.",
                "captain": "The sixth day demands final action. The crisis is upon you, and you must make your last military preparations to protect your kingdom from the coming destruction.",
                "spy": "The sixth day requires final action. The crisis is upon you, and you must make your last covert preparations to protect your kingdom from the coming destruction."
            },
            "day_7": {
                "king": "The seventh day brings the final confrontation. The crisis has arrived, and you must face the coming destruction with whatever preparations you have made.",
                "captain": "The seventh day brings the final battle. The crisis has arrived, and you must face the coming destruction with whatever military preparations you have made.",
                "spy": "The seventh day brings the final operation. The crisis has arrived, and you must face the coming destruction with whatever covert preparations you have made."
            }
        }
    
    def get_dialogue_message(self, role: str, action_type: str, action_id: str, success: bool) -> str:
        """Get dialogue message for specific role and action"""
        key = f"{role}_{action_id}_{'success' if success else 'failure'}"
        dialogue = self.dialogue_content.get(key)
        
        if dialogue:
            if success:
                message = random.choice(dialogue.success_messages)
            else:
                message = random.choice(dialogue.failure_messages)
        else:
            # Fallback to neutral message
            key = f"{role}_{action_id}_success"
            dialogue = self.dialogue_content.get(key)
            if dialogue:
                message = random.choice(dialogue.neutral_messages)
            else:
                message = f"{role} performs {action_id} with {'success' if success else 'failure'}."
        
        # Enhance message with additional context
        enhanced_message = self._enhance_dialogue_message(message, role, action_type, action_id, success)
        return enhanced_message
    
    def _enhance_dialogue_message(self, base_message: str, role: str, action_type: str, action_id: str, success: bool) -> str:
        """Enhance dialogue message with additional context and details"""
        enhanced_parts = [base_message]
        
        # Add time context
        time_contexts = [
            "The morning light filters through the windows as you complete this task.",
            "The afternoon sun casts long shadows as you finish your work.",
            "Evening approaches as you conclude this important action.",
            "The day progresses as you carry out this duty.",
            "Time moves forward as you fulfill your responsibilities."
        ]
        enhanced_parts.append(random.choice(time_contexts))
        
        # Add role-specific context
        if role == "king":
            role_contexts = [
                "As the ruler of this kingdom, your decisions carry great weight.",
                "Your royal authority allows you to command resources and attention.",
                "The court watches your every move, seeking guidance and leadership.",
                "Your position grants you access to the kingdom's finest resources.",
                "The weight of the crown reminds you of your responsibilities."
            ]
        elif role == "captain":
            role_contexts = [
                "Your military training and experience guide your actions.",
                "The soldiers under your command look to you for leadership.",
                "Your tactical mind analyzes every situation carefully.",
                "The discipline of military life shapes your approach.",
                "Your reputation as a capable officer precedes you."
            ]
        else:  # spy
            role_contexts = [
                "Your covert training allows you to operate in the shadows.",
                "The network of contacts you've built serves you well.",
                "Your ability to blend in and gather information is unmatched.",
                "The art of deception and stealth guides your methods.",
                "Your secretive nature helps you navigate complex situations."
            ]
        enhanced_parts.append(random.choice(role_contexts))
        
        # Add action-specific context
        if action_type == "resource":
            action_contexts = [
                "Managing resources requires careful planning and foresight.",
                "The kingdom's prosperity depends on wise resource allocation.",
                "Every decision about resources affects the kingdom's future.",
                "Strategic resource management is key to survival.",
                "The careful balance of resources determines success or failure."
            ]
        elif action_type == "preparation":
            action_contexts = [
                "Preparation is the key to overcoming any crisis.",
                "Your foresight and planning may save the kingdom.",
                "Every preparation action brings you closer to victory.",
                "The time spent preparing will not be wasted.",
                "Your preparations strengthen the kingdom's defenses."
            ]
        else:  # investigation
            action_contexts = [
                "Knowledge is power, and investigation reveals the truth.",
                "Every piece of evidence brings you closer to understanding.",
                "The truth lies hidden, waiting to be discovered.",
                "Your investigative skills uncover valuable information.",
                "Each clue you find paints a clearer picture of the crisis."
            ]
        enhanced_parts.append(random.choice(action_contexts))
        
        # Add outcome context
        if success:
            outcome_contexts = [
                "Your efforts have borne fruit, bringing you closer to your goal.",
                "Success in this endeavor strengthens your position.",
                "The positive outcome of this action boosts your confidence.",
                "Your skillful execution of this task impresses those around you.",
                "This successful action brings hope for the kingdom's future."
            ]
        else:
            outcome_contexts = [
                "Despite the setback, you learn valuable lessons from this experience.",
                "Even in failure, you gain insights that will help in the future.",
                "This challenge tests your resolve and determination.",
                "The difficulty of this task reminds you of the stakes involved.",
                "Every obstacle overcome makes you stronger and wiser."
            ]
        enhanced_parts.append(random.choice(outcome_contexts))
        
        return "\n\n".join(enhanced_parts)
    
    def get_random_event_message(self, event_id: str, role: str) -> str:
        """Get random event message for specific role"""
        event_content = self.random_event_content.get(event_id)
        if event_content:
            role_message = event_content.role_specific_messages.get(role)
            if role_message:
                return role_message
            return event_content.description
        return f"Random event {event_id} occurs."
    
    def get_ending_message(self, event_id: str, outcome: str, role: str) -> str:
        """Get ending message for specific event, outcome, and role"""
        key = f"{event_id}_{outcome}"
        ending_content = self.ending_content.get(key)
        if ending_content:
            role_impact = ending_content.role_specific_impact.get(role)
            if role_impact:
                return f"{ending_content.title}\n\n{ending_content.description}\n\n{role_impact}"
            return f"{ending_content.title}\n\n{ending_content.description}"
        return f"Game ended with {outcome} for {event_id}."
    
    def get_daily_narrative(self, day: int, role: str) -> str:
        """Get daily narrative for specific day and role"""
        day_key = f"day_{day}"
        daily_content = self.daily_narratives.get(day_key)
        if daily_content:
            return daily_content.get(role, f"Day {day} begins.")
        return f"Day {day} begins."
    
    def get_random_event_description(self, event_id: str) -> str:
        """Get random event description"""
        event_content = self.random_event_content.get(event_id)
        if event_content:
            return event_content.description
        return f"Random event {event_id} occurs."
    
    def get_random_event_effects_description(self, event_id: str) -> str:
        """Get random event effects description"""
        event_content = self.random_event_content.get(event_id)
        if event_content:
            return event_content.effects_description
        return f"Random event {event_id} has various effects."
