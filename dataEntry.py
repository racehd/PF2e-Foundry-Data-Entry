import regex as re
import pyperclip as cl

def convert_to_lower(match_obj):
    if match_obj.group() is not None:
        return match_obj.group().lower()

def reformat(text):
    ## Initial handling not using regex.
    string = "<p>" + text.replace("’","'").replace("Trigger","<p><strong>Trigger</strong>").replace("Requirements","<p><strong>Requirements</strong>").replace("\nCritical Success","</p><hr /><p><strong>Critical Success</strong>").replace("\nSuccess","</p><p><strong>Success</strong>").replace("\nFailure","</p><p><strong>Failure</strong>").replace("\nCritical Failure","</p><p><strong>Critical Failure</strong>").replace("\nSpecial","</p><p><strong>Special</strong>").replace("\n"," ").replace("Frequency","<p><strong>Frequency</strong>").replace("Effect","</p><p><strong>Effect</strong>").replace("—","-") + "</p>"
    string = string.replace("<p><p>","<p>").replace("–","-").replace("Activate","</p><p><strong>Activate</strong>").replace(r"”",r"\"").replace(r"“",r"\"")
    
    string = string.replace("Maximum Duration","</p><p><strong>Maximum Duration</strong>").replace("Onset","</p><p><strong>Onset</strong>").replace("Saving Throw","</p><p><strong>Saving Throw</strong>")
    string = re.sub(r"Stage (\d)",r"</p><p><strong>Stage \1</strong>",string)
    
    ## Skills and saves
    string = re.sub(r"DC (\d+) basic (\w+) save", r"<span data-pf2-check='\2' data-pf2-traits='damaging-effect' data-pf2-label='' data-pf2-dc='\1' data-pf2-show-dc='gm'>basic \2</span> save",string)
    string = re.sub(r"DC (\d+) (Reflex|Will|Fortitude)", r"<span data-pf2-check='\2' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\1' data-pf2-show-dc='gm'>\2</span>",string)
    string = re.sub(r"(Reflex|Will|Fortitude) DC (\d+)", r"<span data-pf2-check='\1' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\2' data-pf2-show-dc='gm'>\1</span>",string)
    string = re.sub(r"(Reflex|Will|Fortitude) \(DC (\d+)\)", r"<span data-pf2-check='\1' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\2' data-pf2-show-dc='gm'>\1</span>",string)
    string = re.sub(r"(Reflex|Will|Fortitude) save \(DC (\d+)\)", r"<span data-pf2-check='\1' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\2' data-pf2-show-dc='gm'>\1</span>",string)

    string = re.sub(r"DC (\d+) (Perception|Acrobatics|Arcana|Athletics|Crafting|Deception|Diplomacy|Intimidation|Medicine|Nature|Occultism|Performance|Religion|Society|Stealth|Survival|Thievery)", r"<span data-pf2-check='\2' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\1' data-pf2-show-dc='gm'>\2</span>",string)
    string = re.sub(r"(Perception|Acrobatics|Arcana|Athletics|Crafting|Deception|Diplomacy|Intimidation|Medicine|Nature|Occultism|Performance|Religion|Society|Stealth|Survival|Thievery) DC (\d+)", r"<span data-pf2-check='\1' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\2' data-pf2-show-dc='gm'>\1</span>",string)
    string = re.sub(r"(Perception|Acrobatics|Arcana|Athletics|Crafting|Deception|Diplomacy|Intimidation|Medicine|Nature|Occultism|Performance|Religion|Society|Stealth|Survival|Thievery) \(DC (\d+)\)", r"<span data-pf2-check='\1' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\2' data-pf2-show-dc='gm'>\1</span>",string)

    string = re.sub(r"(\w+) Lore DC (\d+)", r"<span data-pf2-check='\2' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\1' data-pf2-show-dc='gm'>\2 Lore</span>",string)
    string = re.sub(r"DC (\d+) (\w+) save", r"<span data-pf2-check='\2' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\1' data-pf2-show-dc='gm'>\2</span> save",string)
    string = re.sub(r"DC (\d+) flat check", r"<span data-pf2-check='flat' data-pf2-traits='' data-pf2-label='' data-pf2-dc='\1' data-pf2-show-dc='owner'>Flat Check</span>",string)

    ## Catch capitalized saves
    string = re.sub("check='(Will|Fortitude|Reflex)'", convert_to_lower, string)
    string = re.sub(r"check='(Perception|Acrobatics|Arcana|Athletics|Crafting|Deception|Diplomacy|Intimidation|Medicine|Nature|Occultism|Performance|Religion|Society|Stealth|Survival|Thievery)'", convert_to_lower, string)
    
    # Damage rolls
    string = re.sub(r" (\d)d(\d) (rounds|minutes|hours|days)", r" [[/r \1d\2 #\3]]{\1d\2 \3}", string)
    string = re.sub(r" (\d+) (\w*) damage", r" [[/r \1 #\2 damage]]{\1 \2}", string)
    string = re.sub(r"(\d+)d(\d+)\+(\d+) (\w*) damage", r"[[/r \1d\2 + \3 #\4]]{\1d\2 + \3 \4 damage}", string)
    string = re.sub(r"(\d+)d(\d+) persistent (\w*) damage", r"[[/r \1d\2 #persistent \3]]{\1d\2} @Compendium[pf2e.conditionitems.Persistent Damage]{Persistent \3 Damage}", string)
    string = re.sub(r"(\d+)d(\d+) (\w*) damage", r"[[/r \1d\2 #\3]]{\1d\2 \3 damage}", string)
    string = re.sub(r"(\d+)d(\d+) (\w+)(\,|\.)", r"[[/r \1d\2 #\3]]{\1d\2 \3}\4", string)
    string = re.sub(r"(\d+)d(\d+)\.", r"[[/r \1d\2]]{\1d\2}.", string)
    
    ## Spell heightening handling
    string = re.sub(r"Heightened \(",r"<hr />Heightened (",string, count = 1)
    string = re.sub(r"Heightened \(\+(\d+)\)",r"</p><p><strong>Heightened (+\1)</strong>",string)
    string = re.sub(r"Heightened \((\d+)(\w+)\)",r"</p><p><strong>Heightened (\1\2)</strong>",string)
    string = re.sub(r"<hr /></p><p><strong>Heightened",r"</p><hr /><p><strong>Heightened",string)
        
    ## Removing bullet points, should replace with the actual bullet points.
    string = re.sub(r"•","<ul><li>",string, count = 1)
    string = re.sub(r"•","</li><li>",string)
    
    # ## Add template buttons
    # string = re.sub(r"(\d+)-foot (emanation|burst)",r"<span data-pf2-effect-area='\2\' data-pf2-distance='\1'>\1-foot \2</span>",string)
    # string = re.sub(r"(\d+)-foot cone",r"<span data-pf2-effect-area='cone' data-pf2-distance='\1'>\1-foot Cone</span>",string)
    # string = re.sub(r"(\d+)-foot line",r"<span data-pf2-effect-area='line' data-pf2-distance='\1'>\1-foot Line</span>",string)
    
    ## Condition handling
    string = re.sub(r"blinded", r"@Compendium[pf2e.conditionitems.Blinded]{Blinded}",string, count = 1)
    string = re.sub(r"confused", r"@Compendium[pf2e.conditionitems.Confused]{Confused}",string, count = 1)
    string = re.sub(r"concealed", r"@Compendium[pf2e.conditionitems.Concealed]{Concealed}",string, count = 1)
    string = re.sub(r"dazzled", r"@Compendium[pf2e.conditionitems.Dazzled]{Dazzled}",string, count = 1)
    string = re.sub(r"deafened", r"@Compendium[pf2e.conditionitems.Deafened]{Deafened}",string, count = 1)
    string = re.sub(r"invisible", r"@Compendium[pf2e.conditionitems.Invisible]{Invisible}",string, count = 1)
    string = re.sub(r"flat footed", r"@Compendium[pf2e.conditionitems.Flat-Footed]{Flat-Footed}",string, count = 1)
    string = re.sub(r"flat-footed", r"@Compendium[pf2e.conditionitems.Flat-Footed]{Flat-Footed}",string, count = 1)
    string = re.sub(r"immobilized", r"@Compendium[pf2e.conditionitems.Immobilized]{Immobilized}",string, count = 1)
    string = re.sub(r"prone", r"@Compendium[pf2e.conditionitems.Prone]{Prone}",string, count = 1)
    string = re.sub(r"unconscious", r"@Compendium[pf2e.conditionitems.Unconscious]{Unconscious}",string, count = 1)
    string = re.sub(r"fascinated", r"@Compendium[pf2e.conditionitems.Fascinated]{Fascinated}",string, count = 1)
    string = re.sub(r"paralyzed", r"@Compendium[pf2e.conditionitems.Paralyzed]{Paralyzed}",string, count = 1)
    
    string = re.sub(r"clumsy 1", r"@Compendium[pf2e.conditionitems.Clumsy]{Clumsy 1}",string, count = 1)
    string = re.sub(r"doomed 1", r"@Compendium[pf2e.conditionitems.Doomed]{Doomed 1}",string, count = 1)
    string = re.sub(r"drained 1", r"@Compendium[pf2e.conditionitems.Drained]{Drained 1}",string, count = 1)
    string = re.sub(r"enfeebled 1", r"@Compendium[pf2e.conditionitems.Enfeebled]{Enfeebled 1}",string, count = 1)
    string = re.sub(r"slowed 1", r"@Compendium[pf2e.conditionitems.Slowed]{Slowed 1}",string, count = 1)
    string = re.sub(r"frightened 1", r"@Compendium[pf2e.conditionitems.Frightened]{Frightened 1}",string, count = 1)
    string = re.sub(r"sickened 1", r"@Compendium[pf2e.conditionitems.Sickened]{Sickened 1}",string, count = 1)
    string = re.sub(r"stunned 1", r"@Compendium[pf2e.conditionitems.Stunned]{Stunned 1}",string, count = 1)    
    string = re.sub(r"stupefied 1", r"@Compendium[pf2e.conditionitems.Stupefied]{Stupefied 1}",string, count = 1)
    string = re.sub(r"quickened 1", r"@Compendium[pf2e.conditionitems.Quickened]{Quickened 1}",string, count = 1)
    
    string = re.sub(r"clumsy 2", r"@Compendium[pf2e.conditionitems.Clumsy]{Clumsy 2}",string, count = 1)
    string = re.sub(r"doomed 2", r"@Compendium[pf2e.conditionitems.Doomed]{Doomed 2}",string, count = 1)
    string = re.sub(r"drained 2", r"@Compendium[pf2e.conditionitems.Drained]{Drained 2}",string, count = 1)
    string = re.sub(r"enfeebled 2", r"@Compendium[pf2e.conditionitems.Enfeebled]{Enfeebled 2}",string, count = 1)
    string = re.sub(r"slowed 2", r"@Compendium[pf2e.conditionitems.Slowed]{Slowed 2}",string, count = 1)
    string = re.sub(r"frightened 2", r"@Compendium[pf2e.conditionitems.Frightened]{Frightened 2}",string, count = 1)
    string = re.sub(r"sickened 2", r"@Compendium[pf2e.conditionitems.Sickened]{Sickened 2}",string, count = 1)
    string = re.sub(r"stunned 2", r"@Compendium[pf2e.conditionitems.Stunned]{Stunned 2}",string, count = 1)    
    string = re.sub(r"stupefied 2", r"@Compendium[pf2e.conditionitems.Stupefied]{Stupefied 2}",string, count = 1)
    string = re.sub(r"quickened 2", r"@Compendium[pf2e.conditionitems.Quickened]{Quickened 2}",string, count = 1)
    
    string = re.sub(r"clumsy 3", r"@Compendium[pf2e.conditionitems.Clumsy]{Clumsy 3}",string, count = 1)
    string = re.sub(r"doomed 3", r"@Compendium[pf2e.conditionitems.Doomed]{Doomed 3}",string, count = 1)
    string = re.sub(r"drained 3", r"@Compendium[pf2e.conditionitems.Drained]{Drained 3}",string, count = 1)
    string = re.sub(r"enfeebled 3", r"@Compendium[pf2e.conditionitems.Enfeebled]{Enfeebled 3}",string, count = 1)
    string = re.sub(r"slowed 3", r"@Compendium[pf2e.conditionitems.Slowed]{Slowed 3}",string, count = 1)
    string = re.sub(r"frightened 3", r"@Compendium[pf2e.conditionitems.Frightened]{Frightened 3}",string, count = 1)
    string = re.sub(r"sickened 3", r"@Compendium[pf2e.conditionitems.Sickened]{Sickened 3}",string, count = 1)
    string = re.sub(r"stunned 3", r"@Compendium[pf2e.conditionitems.Stunned]{Stunned 3}",string, count = 1)    
    string = re.sub(r"stupefied 3", r"@Compendium[pf2e.conditionitems.Stupefied]{Stupefied 3}",string, count = 1)

    string = re.sub(r"clumsy 4", r"@Compendium[pf2e.conditionitems.Clumsy]{Clumsy 4}",string, count = 1)
    string = re.sub(r"doomed 4", r"@Compendium[pf2e.conditionitems.Doomed]{Doomed 4}",string, count = 1)
    string = re.sub(r"drained 4", r"@Compendium[pf2e.conditionitems.Drained]{Drained 4}",string, count = 1)
    string = re.sub(r"enfeebled 4", r"@Compendium[pf2e.conditionitems.Enfeebled]{Enfeebled 4}",string, count = 1)
    string = re.sub(r"slowed 4", r"@Compendium[pf2e.conditionitems.Slowed]{Slowed 4}",string, count = 1)
    string = re.sub(r"frightened 4", r"@Compendium[pf2e.conditionitems.Frightened]{Frightened 4}",string, count = 1)
    string = re.sub(r"sickened 4", r"@Compendium[pf2e.conditionitems.Sickened]{Sickened 4}",string, count = 1)
    string = re.sub(r"stunned 4", r"@Compendium[pf2e.conditionitems.Stunned]{Stunned 4}",string, count = 1)    
    string = re.sub(r"stupefied 4", r"@Compendium[pf2e.conditionitems.Stupefied]{Stupefied 4}",string, count = 1)

    # Comment out when not entering backgrounds.
    # string = re.sub(r"Choose two ability boosts.",r"</p><p>Choose two ability boosts.",string)
    # string = re.sub(r"(Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma)",r"<strong>\1</strong>",string, count = 2)
    # string = re.sub(r"You're trained in",r"</p><p>You're trained in",string)

    print("\n")
    print(string)
    cl.copy(string)

reformat(input())

