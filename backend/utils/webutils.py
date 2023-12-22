from utils.db import (
	find_law_projects_for_deputy,
	find_operational_expenses_for_deputy,
	find_operational_indicators_by_category_and_month,
	find_staff_expenses_for_deputy,
	find_support_staff_indicators_by_month,
	find_deputy_periods,
	find_deputy_votings,
	find_last_N_months_with_records,
	find_operational_ranking_by_month,
	find_operational_indicators_by_month,
	find_support_staff_ranking_by_month,
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
		"updateTimestamp": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
		"beacon": {
			"chainId": chain_id,
			"pulseId": pulse_id,
		},
		"profile": {
			"name": profile["first_name"],
			"firstSurname": profile["first_surname"],
			"secondSurname": profile["second_surname"],
			"picture": profile["profile_picture"],
			"gender": profile["gender"],
			"birthdate": profile["birthdate"],
			"profession": profile["profession"],
			"district": profile["district"],
			"region": profile["district_region"],
			"communes": profile["district_communes"],
			"party": profile["party"],
			"partyAlias": profile["party_alias"],
			"twitterUsername": profile["twitter_username"],
			"instagramUsername": profile["instagram_username"],
			"periods": find_deputy_periods(deputy_index),
		},
		"attendance": None if not attendance else {
			"attended": attendance["present"],
			"justifiedAbsent": attendance["justified_absent"],
			"unjustifiedAbsent": attendance["unjustified_absent"],
			"total": attendance["total"],
		},
		"expenses": build_expenses_by_month(deputy_index),
		"activity": {
			"inProcess": len(list(filter(lambda x: x["status"] == "En tramitación", law_projects))),
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
			"votingId": row[1],
			"votingDate": row[2],
			"bulletinNumber": row[3],
			"documentTitle": row[4],
			"articleText": row[5],
			"voted": row[6],
			"totalApproved": row[7], 
			"totalRejected": row[8],
			"totalAbstention": row[9],
			"result": row[10],
		}
		votings.append(voting)
	return votings


def build_expenses_by_month(deputy_id: int):
	months_limit = 6
	months_limit = 8
	# Obtain the last N months with records
	months = find_last_N_months_with_records(months_limit, 'expenses_operational', deputy_id)
	# Obtain saved expenses for deputy
	op_exp = find_operational_expenses_for_deputy(deputy_id)
	st_exp = find_staff_expenses_for_deputy(deputy_id)
	expenses = []

	# Build expenses JSON by month
	for month in months:
		[year, month_num] = month[0:2]
		month_total = 0

		month_record = {
			"code": int("{}{:02d}{}".format(year, month_num, deputy_id)),
			"year": year,
			"month": MONTHS[month_num-1],
			"detail" : []
		}
		month_filtered_op_exp = list(
			filter(lambda x: x[1] == year and x[2] == month_num, op_exp)
		)
		month_filtered_st_exp = list(
			filter(lambda x: x[1] == year and x[2] == month_num, st_exp)
		)

		# Staff expenses for deputy
		average, minimum, maximum = find_support_staff_indicators_by_month(year, month_num)
		ranking = find_support_staff_ranking_by_month(deputy_id, year, month_num)
		staff_amount = 0

		if month_filtered_st_exp:
			register = month_filtered_st_exp[0]
			[quantity, amount] = register[3:5]
			staff_amount = amount
			month_total += amount
			month_record["detail"].append({
				"type": "Personal de Apoyo",
				"amount": amount,
				"supportStaff": quantity,
				"deputiesRanking": ranking,
				"deputiesAvg": round(average),
				"deputiesMin": minimum,
				"deputiesMax": maximum,
			})
		else:
			month_record["detail"].append({
				"type": "Personal de Apoyo",
				"amount": None,
				"supportStaff": None,
				"deputiesRanking": ranking,
				"deputiesAvg": round(average) if average else None,
				"deputiesMin": minimum if minimum else None,
				"deputiesMax": maximum if maximum else None,
			})
		
		# Operational expenses for deputy
		operational_expenses = []
		for op_exp_record in month_filtered_op_exp:
			[category, amount] = op_exp_record[3:5]
			month_total += amount
			average, minimum, maximum = find_operational_indicators_by_category_and_month(category, year, month_num)
			operational_expenses.append({
				"subtype": category,
				"amount": amount,
				"deputiesAvg": round(average),
				"deputiesMin": minimum,
				"deputiesMax": maximum,
			})
		operational_ranking = find_operational_ranking_by_month(deputy_id, year, month_num)
		op_avg, op_min, op_max = find_operational_indicators_by_month(year, month_num)
		month_record["detail"].append({
			"type": "Operacional",
			"amount": month_total - staff_amount,
			"deputiesRanking": operational_ranking,
			"deputiesAvg": round(op_avg),
			"deputiesMin": op_min,
			"deputiesMax": op_max,
			"expenses": operational_expenses,
		})

		month_record["total"] = month_total
		expenses.append(month_record)

	return expenses
