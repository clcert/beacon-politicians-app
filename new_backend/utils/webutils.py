from utils.db import (
	find_law_projects_for_deputy,
	find_operational_expenses_for_deputy,
	find_operative_indicators_by_category_and_month,
	find_staff_expenses_for_deputy,
	find_support_staff_indicators_by_month,
)
from utils.data import MONTHS, DEPUTIES_JSON_PATH
from utils.utils import get_json_data

import json


def generate_deputy_json_data(deputy, timestamp, chain_id, pulse_id):
	"""
	Generates a JSON file with the deputy's data for the given timestamp
    to be used in the frontend application, without needing to load the
    entire database for each request.
	"""

	profile = deputy.profile
	attendance = deputy.attendance
	deputy_index = deputy.real_index

	law_projects = load_law_projects(deputy_index)

	current_deputies = get_json_data()
	if not current_deputies:
		current_deputies = {"records": {}}

	record = {
		"index": deputy_index,
		"beacon": {
			"chainId": chain_id,
			"pulseId": pulse_id,
		},
		"profile": {
			"name": profile["first_name"],
			"1st_surname": profile["first_surname"],
			"2nd_surname": profile["second_surname"],
			"picture": profile["profile_picture"],
			"gender": profile["party"],
			"birthdate": profile["birthdate"],
			"profession": profile["profession"],
			"district": profile["district"],
			"region": profile["district_region"],
			"party": profile["party"],
			"party_alias": profile["party_alias"],
		},
		"attendance": {
			"assisted": attendance["present"],
			"justified_absent": attendance["justified_absent"],
			"unjustified_absent": attendance["unjustified_absent"],
			"total": attendance["total"],
		},
		"expenses": {
			"description": "Expenses of the last 6 months with records.",
			"operative": load_operative_expenses(deputy_index),
			"staff": load_staff_expenses(deputy_index),
		},
		"activity": {
			"description": "Law projects presented by the deputy.",
			"law_projects": law_projects,
			"statistics": {
				"in_process": len(list(filter(lambda x: x["status"] == "En tramitación", law_projects))),
				"published": len(list(filter(lambda x: x["status"] == "Publicado", law_projects))),
				"archived": len(list(filter(lambda x: x["status"] == "Archivado", law_projects))),
				"withdrawn": len(list(filter(lambda x: x["status"] == "Retirado", law_projects))),
				"rejected": len(list(filter(lambda x: x["status"] == "Rechazado", law_projects))),
				"unadmissible": len(list(filter(lambda x: x["status"] == "Inadmisible", law_projects))),
				"unconstitutional": len(list(filter(lambda x: x["status"] == "Inconstitucional", law_projects))),
				"all": len(law_projects),
			},
		},
	}
	current_deputies["records"][timestamp.strftime("%Y-%m-%d")] = record

	with open(DEPUTIES_JSON_PATH, "w", encoding="utf-8") as outfile:
		json.dump(current_deputies, outfile, indent=4, ensure_ascii=False)
		outfile.close()
	
	return record


def load_law_projects(deputy_id):
	projects = find_law_projects_for_deputy(deputy_id)
	law_projects = []
	for project in projects:
		project_dict = {
			"date": project[1],
			"title": project[2],
			"status": project[4],
		}
		law_projects.append(project_dict)
	return law_projects


def load_operative_expenses(deputy_id):
	op_exp = find_operational_expenses_for_deputy(deputy_id)
	registered_months = []
	expenses = {}

	for register in op_exp:
		year, month = register[1], register[2]
		category = register[3]

		month_reg = "{}-{:02d}".format(year, MONTHS.index(month) + 1)
		if month_reg not in registered_months:
			registered_months.append(month_reg)
			expenses[month_reg] = {}

		average, minimum, maximum = find_operative_indicators_by_category_and_month(category, year, month)
		expenses[month_reg][category] = {
			"amount": register[4],
			"deputies_avg": average,
			"deputies_min": minimum,
			"deputies_max": maximum,
		}
	return expenses


def load_staff_expenses(deputy_id):
	st_exp = find_staff_expenses_for_deputy(deputy_id)
	expenses = {}

	for register in st_exp:
		year, month = register[1], register[2]
		month_reg = "{}-{:02d}".format(year, MONTHS.index(month) + 1)
		average, minimum, maximum = find_support_staff_indicators_by_month(year, month)
		expenses[month_reg] = {
			"total_amount": register[4],
			"support_staff": register[3],
			"deputies_avg": average,
			"deputies_min": minimum,
			"deputies_max": maximum,
		}
	return expenses