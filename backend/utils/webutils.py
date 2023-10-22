from utils.db import (
	find_law_projects_for_deputy,
	find_operational_expenses_for_deputy,
	find_operational_indicators_by_category_and_month,
	find_staff_expenses_for_deputy,
	find_support_staff_indicators_by_month,
	find_deputy_periods,
	find_deputy_votings,
	find_last_N_months_with_records,
)
from utils.data import DEPUTIES_JSON_PATH, MONTHS
from utils.utils import get_json_data

from datetime import datetime

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
		current_deputies = {"records": []}

	# Check if the deputy is already in the JSON file
	current_deputies["records"] = list(
		filter(lambda x: x["date"] != timestamp.strftime('%Y-%m-%d'), current_deputies["records"])
	)

	record = {
		"index": deputy_index,
		"date": timestamp.strftime('%Y-%m-%d'),
		"update_timestamp": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
		"beacon": {
			"chainId": chain_id,
			"pulseId": pulse_id,
		},
		"profile": {
			"name": profile["first_name"],
			"first_surname": profile["first_surname"],
			"second_surname": profile["second_surname"],
			"picture": profile["profile_picture"],
			"gender": profile["gender"],
			"birthdate": profile["birthdate"],
			"profession": profile["profession"],
			"district": profile["district"],
			"region": profile["district_region"],
			"party": profile["party"],
			"party_alias": profile["party_alias"],
			"periods": find_deputy_periods(deputy_index),
		},
		"attendance": None if not attendance else {
			"attended": attendance["present"],
			"justified_absent": attendance["justified_absent"],
			"unjustified_absent": attendance["unjustified_absent"],
			"total": attendance["total"],
		},
		"expenses": build_expenses_by_month(deputy_index),
		"activity": {
			"in_process": len(list(filter(lambda x: x["status"] == "En tramitación", law_projects))),
			"published": len(list(filter(lambda x: x["status"] == "Publicado", law_projects))),
			"archived": len(list(filter(lambda x: x["status"] == "Archivado", law_projects))),
			"withdrawn": len(list(filter(lambda x: x["status"] == "Retirado", law_projects))),
			"rejected": len(list(filter(lambda x: x["status"] == "Rechazado", law_projects))),
			"unadmissible": len(list(filter(lambda x: x["status"] == "Inadmisible", law_projects))),
			"unconstitutional": len(list(filter(lambda x: x["status"] == "Inconstitucional", law_projects))),
			"all": len(law_projects),
		},
		"votings": load_deputy_votings(deputy_index),
	}
	current_deputies["records"].append(record)
	current_deputies["records"].sort(key=lambda dep: dep['date'])
	current_deputies["records"] = current_deputies["records"][-14:]

	with open(DEPUTIES_JSON_PATH, "w", encoding="utf-8") as outfile:
		json.dump(current_deputies, outfile, indent=4, ensure_ascii=False)
		outfile.close()
	
	return record


def load_law_projects(deputy_id):
	projects = find_law_projects_for_deputy(deputy_id)
	law_projects = []
	for project in projects:
		project_dict = {
			"bulletin": project[1],
			"title": project[2],
			"status": project[4],
		}
		law_projects.append(project_dict)
	return law_projects


def load_deputy_votings(deputy_id):
	rows = find_deputy_votings(deputy_id)
	votings = []
	for row in rows:
		voting = {
			"voting_id": row[1],
			"voting_date": row[2],
			"bulletin_number": row[3],
			"document_title": row[4],
			"article_text": row[5],
			"voted": row[6],
			"total_approved": row[7], 
			"total_rejected": row[8],
			"total_abstention": row[9],
			"result": row[10],
		}
		votings.append(voting)
	return votings


def build_expenses_by_month(deputy_id: int):
	months_limit = 6
	months = find_last_N_months_with_records(months_limit, 'expenses_operational', deputy_id)
	op_exp = find_operational_expenses_for_deputy(deputy_id)
	st_exp = find_staff_expenses_for_deputy(deputy_id)
	expenses = []

	for month in months:
		[year, month_num] = month[0:2]
		month_total = 0

		month_record = {
			"code": int("{}{:02d}{}".format(year, month_num, deputy_id)),
			"year": year,
			"month": MONTHS[month_num-1],
		}
		month_filtered_op_exp = list(
			filter(lambda x: x[1] == year and x[2] == month_num, op_exp)
		)
		month_filtered_st_exp = list(
			filter(lambda x: x[1] == year and x[2] == month_num, st_exp)
		)
		average, minimum, maximum = find_support_staff_indicators_by_month(year, month_num)
		if month_filtered_st_exp:
			register = month_filtered_st_exp[0]
			[quantity, amount] = register[3:5]
			month_total += amount
			month_record["Personal de Apoyo"] = {
				"amount": amount,
				"support_staff": quantity,
				"deputies_avg": average,
				"deputies_min": minimum,
				"deputies_max": maximum,
			}
		else:
			month_record["Personal de Apoyo"] = {
				"amount": None,
				"support_staff": None,
				"deputies_avg": average,
				"deputies_min": minimum,
				"deputies_max": maximum,
			}
		
		for op_exp_record in month_filtered_op_exp:
			[category, amount] = op_exp_record[3:5]
			month_total += amount
			average, minimum, maximum = find_operational_indicators_by_category_and_month(category, year, month_num)
			month_record[category] = {
				"amount": amount,
				"deputies_avg": average,
				"deputies_min": minimum,
				"deputies_max": maximum,
			}

		month_record["total"] = month_total
		expenses.append(month_record)
	
	return expenses
