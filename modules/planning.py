def inr(value):
    value = float(value)
    if value >= 10_000_000:
        return f"₹{value / 10_000_000:.2f} Cr"
    if value >= 100_000:
        return f"₹{value / 100_000:.2f} L"
    return f"₹{value:,.0f}"

def estimate_project(structure, area, tier, completion, land_area, construction_rate, valuation_rate,
                     steel_kg_per_sqft, cement_bags_per_sqft, location=""):
    area = float(area)
    completion = float(completion)
    construction_rate = float(construction_rate)
    valuation_rate = float(valuation_rate)
    budget = area * construction_rate
    capex = budget * completion / 100.0
    valuation = area * valuation_rate
    steel_kg = area * float(steel_kg_per_sqft)
    cement_bags = area * float(cement_bags_per_sqft)
    # Tier multiplier is surfaced for context but the user-entered rates drive the calculation.
    tier_note = {"Tier 1": "Metro / higher-cost market", "Tier 2": "Mid-sized city", "Tier 3": "Smaller city / town"}.get(tier, "")
    return {
        "structure_type": structure,
        "built_up_area_sqft": int(area),
        "city_tier": tier,
        "city_tier_context": tier_note,
        "location": location or "Not specified",
        "completion_percent": int(completion),
        "assumptions": {
            "construction_rate_inr_per_sqft": construction_rate,
            "valuation_rate_inr_per_sqft": valuation_rate,
            "steel_kg_per_sqft": float(steel_kg_per_sqft),
            "cement_bags_per_sqft": float(cement_bags_per_sqft),
            "calculation_note": "User-editable thumb rules; replace with local tender rates and engineer-approved quantities."
        },
        "project_budget_inr": round(budget, 2),
        "capex_incurred_inr": round(capex, 2),
        "remaining_budget_inr": round(max(0, budget - capex), 2),
        "market_valuation_inr": round(valuation, 2),
        "steel_requirement_tonnes": round(steel_kg / 1000.0, 2),
        "cement_requirement_bags": round(cement_bags),
        "formatted": {
            "project_budget": inr(budget),
            "capex_incurred": inr(capex),
            "remaining_budget": inr(max(0, budget - capex)),
            "market_valuation": inr(valuation)
        }
    }
