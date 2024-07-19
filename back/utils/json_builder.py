from utils.utils import MONTHS, JSON_PATH
from models.models import Attendance, DailyDeputy, DeputyVoting, Deputy, DeputyPeriod, DeputyProject, OperationalExpense, SupportStaffExpense, LawProject
from datetime import datetime
from os import path, stat
import json



def get_json_data(file_path=JSON_PATH):
    """
    Returns an ordered list of dictionaries containing the date, index from the deputies list and the beacon id,
    ordered according to the date.
    :return:
    """    
    if path.exists(file_path) and stat(file_path).st_size != 0:
        with open(file_path, 'r', encoding='utf-8') as infile:
            try:
                json_data = json.load(infile)
                return json_data
            except (json.decoder.JSONDecodeError, ValueError) as err:
                print(err)
                return None
    return None

def generate_deputy_json_data(daily_deputy: DailyDeputy):
    """
    Generates a JSON file with the deputy's data for the given timestamp
    to be used in the frontend application, without needing to load the
    entire database for each request.
    """
    deputy_id = daily_deputy.deputy_id
    deputy = Deputy.get_by_id(deputy_id)
    periods = DeputyPeriod.get_by_deputy_id(deputy_id)
    votings = DeputyVoting.get_by_deputy_id(deputy_id)
    deputy_projects = DeputyProject.get_by_deputy_id(deputy_id)
    attendance = Attendance.get_by_deputy_id(deputy_id).first()
    operational = OperationalExpense.get_by_deputy_id(deputy_id)
    support_staff = SupportStaffExpense.get_by_deputy_id(deputy_id)

    current_deputies = get_json_data()
    if not current_deputies:
        current_deputies = {"records": []}

    # Check if the deputy is already in the JSON file
    current_deputies["records"] = list(
        filter(lambda x: x["date"] != daily_deputy.date, current_deputies["records"])
    )

    record = {}

    record["index"] = deputy.id
    record["date"] = daily_deputy.date
    record["updateTimestamp"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    record["beacon"] = {
        "chainId": daily_deputy.chain_index,
        "pulseId": daily_deputy.pulse_index,
    }
    record["profile"] = {
        "name": deputy.name,
        "firstSurname": deputy.father_surname,
        "secondSurname": deputy.mother_surname,
        "picture": "",
        "gender": deputy.gender,
        "birthdate": deputy.birth_date,
        "profession": deputy.profession,
        "district": deputy.district_number,
        "region": deputy.district_region,
        "communes": deputy.district_communes,
        "party": deputy.party_name,
        "partyAlias": deputy.party_acronym,
        "twitterUsername": deputy.twitter_usr,
        "instagramUsername": deputy.instagram_usr,
        "periods": list(map(lambda period: [ period.start_date, period.end_date], periods)),
    }
    record["attendance"] = {
        "total": attendance.total_sessions,
        "present": attendance.total_attended,
        "justified": attendance.total_justified,
        "unjustified": attendance.total_unjustified,
        "lastUpdate": attendance.updated_at,
    }

    record["expenses"] = { }


    filter_by_status = lambda status: deputy_projects.filter(LawProject.status == status)
    record["activity"] = {
        "inProcess": filter_by_status("En tramitación").count(),
        "published": filter_by_status("Publicado").count(),
        "archived": filter_by_status("Archivado").count(),
        "withdrawn": filter_by_status("Retirado").count(),
        "rejected": filter_by_status("Rechazado").count(),
        "unadmissible": filter_by_status("Inadmisible").count(),
        "unconstitutional": filter_by_status("Inconstitucional").count(),
        "all": deputy_projects.count(),
    }

    print(votings.count())
    record["votings"] = [
        {
            "votingId": voting.id,
            "votingDate": voting.document.date,
            "bulletinNumber": voting.document.bulletin_id,
            "documentTitle": voting.document.title,
			"articleText": voting.document.description,
			"voted": voting.vote,
			"totalApproved": voting.document.approval_votes, 
			"totalRejected": voting.document.rejection_votes,
			"totalAbstention": voting.document.abstention_votes,
			"result": voting.document.status,
        } for voting in votings
    ]

    current_deputies["records"].append(record)
    current_deputies["records"].sort(key=lambda dep: dep['date'])
    current_deputies["records"] = current_deputies["records"][-14:]

    with open(JSON_PATH, "w", encoding="utf-8") as outfile:
        json.dump(current_deputies, outfile, indent=4, ensure_ascii=False)
        outfile.close()
    
    return record


# def build_expenses_by_month(deputy_id: int):
#     months_limit = 6
#     # Obtain the last N months with records
#     months = find_last_N_months_with_records(months_limit, 'expenses_operational', deputy_id)
#     # Obtain saved expenses for deputy
#     op_exp = find_operational_expenses_for_deputy(deputy_id)
#     st_exp = find_staff_expenses_for_deputy(deputy_id)
#     expenses = []

#     # Build expenses JSON by month
#     for month in months:
#         [year, month_num] = month[0:2]
#         month_total = 0

#         month_record = {
#             "code": int("{}{:02d}{}".format(year, month_num, deputy_id)),
#             "year": year,
#             "month": MONTHS[month_num-1],
#             "detail" : []
#         }
#         month_filtered_op_exp = list(
#             filter(lambda x: x[1] == year and x[2] == month_num, op_exp)
#         )
#         month_filtered_st_exp = list(
#             filter(lambda x: x[1] == year and x[2] == month_num, st_exp)
#         )

#         # Staff expenses for deputy
#         average, minimum, maximum = find_support_staff_indicators_by_month(year, month_num)
#         ranking = find_support_staff_ranking_by_month(deputy_id, year, month_num)
#         staff_amount = 0

#         if month_filtered_st_exp:
#             register = month_filtered_st_exp[0]
#             [quantity, amount] = register[3:5]
#             staff_amount = amount
#             month_total += amount
#             month_record["detail"].append({
#                 "type": "Personal de Apoyo",
#                 "amount": amount,
#                 "supportStaff": quantity,
#                 "deputiesRanking": ranking,
#                 "deputiesAvg": round(average),
#                 "deputiesMin": minimum,
#                 "deputiesMax": maximum,
#             })
#         else:
#             month_record["detail"].append({
#                 "type": "Personal de Apoyo",
#                 "amount": None,
#                 "supportStaff": None,
#                 "deputiesRanking": ranking,
#                 "deputiesAvg": round(average) if average else None,
#                 "deputiesMin": minimum if minimum else None,
#                 "deputiesMax": maximum if maximum else None,
#             })
        
#         # Operational expenses for deputy
#         operational_expenses = []
#         for op_exp_record in month_filtered_op_exp:
#             [category, amount] = op_exp_record[3:5]
#             month_total += amount
#             average, minimum, maximum = find_operational_indicators_by_category_and_month(category, year, month_num)
#             operational_expenses.append({
#                 "subtype": category,
#                 "amount": amount,
#                 "deputiesAvg": round(average),
#                 "deputiesMin": minimum,
#                 "deputiesMax": maximum,
#             })
#         operational_ranking = find_operational_ranking_by_month(deputy_id, year, month_num)
#         op_avg, op_min, op_max = find_operational_indicators_by_month(year, month_num)
#         month_record["detail"].append({
#             "type": "Operacional",
#             "amount": month_total - staff_amount,
#             "deputiesRanking": operational_ranking,
#             "deputiesAvg": round(op_avg),
#             "deputiesMin": op_min,
#             "deputiesMax": op_max,
#             "expenses": operational_expenses,
#         })

#         month_record["total"] = month_total
#         expenses.append(month_record)

#     return expenses
