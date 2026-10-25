def weather_advisory(condition):
    advisories = {
        "High Wind": {
            "level": "High",
            "headline": "High-wind precautions: assess lifting and work-at-height activities before proceeding.",
            "actions": [
                "Suspend crane, hoist, scaffold, and work-at-height operations when site limits or manufacturer limits are exceeded.",
                "Secure loose materials, sheets, temporary barriers, and tools; restrict access to exposed areas.",
                "Check official weather alerts and the approved lifting plan before restarting."
            ]
        },
        "Heavy Rain": {
            "level": "High",
            "headline": "Heavy-rain precautions: protect people, excavations, electrical systems, and fresh concrete.",
            "actions": [
                "Inspect excavation stability, access routes, drainage, and water accumulation; keep personnel clear of unstable excavations.",
                "Isolate electrical equipment in wet or flooded areas and have a qualified electrician inspect before re-energizing.",
                "Protect fresh concrete from washout and follow the approved mix, placement, and curing method statement.",
                "Pause work where visibility, access, or ground stability is unsafe."
            ]
        },
        "Extreme Heat": {
            "level": "High",
            "headline": "Heat-stress precautions: adjust work planning and monitor workers.",
            "actions": [
                "Schedule strenuous work for cooler hours where practicable and provide shaded rest areas.",
                "Provide accessible drinking water and enforce rest/work cycles based on the site heat-stress plan.",
                "Train supervisors to recognize heat exhaustion and heat stroke; activate the site emergency plan if symptoms appear.",
                "Follow the concrete supplier's and engineer's hot-weather placement and curing procedures."
            ]
        },
        "Normal": {
            "level": "Routine",
            "headline": "Routine conditions selected: continue only under the approved site safety and quality plans.",
            "actions": [
                "Conduct the daily toolbox talk, PPE checks, housekeeping inspection, and equipment pre-start checks.",
                "Verify permits, method statements, access controls, and material inspection records.",
                "Maintain curing and inspection records and monitor updated weather alerts."
            ]
        }
    }
    return advisories.get(condition, advisories["Normal"])
