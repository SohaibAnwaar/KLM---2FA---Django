from klm.intelligence.neo4j.neo4j_client import Neo4jDriver


def convert_n4jtime_to_string(records: list):
    for record in records:
        item = record["timestamp"]
        record["timestamp"] = str(item)


def query_significant_event_today_alerts(db_driver: Neo4jDriver):
    query = """
MATCH (a: Alert)
WHERE toString(a.timestamp) CONTAINS toString(date())
RETURN a
ORDER BY a.timestamp DESC, abs(a.change_magnitude)
"""
    result = db_driver.execute_query(query=query)
    result = [dict(res["a"]) for res in result]
    convert_n4jtime_to_string(result)
    return result


def query_significant_event_curr_alerts(db_driver: Neo4jDriver):
    query = """
MATCH (alert: Alert)
WITH alert.title AS uniqueTitle, alert
ORDER BY alert.timestamp DESC
WITH uniqueTitle, COLLECT(alert) AS alertNodes
WITH alertNodes[0] as a
RETURN a, toString(a.timestamp) as timestamp_string
ORDER BY a.timestamp DESC, abs(a.change_magnitude)
"""
    result = db_driver.execute_query(query=query)
    result = [dict(res["a"]) for res in result]
    convert_n4jtime_to_string(result)
    return result


def data_lineage_province(db_driver: Neo4jDriver, region_name: str, region_code: str):
    query = f"""
        MATCH (r:Region {{region_name: '{region_name}', region_code: '{region_code}'}})-[:HAS_VIOSCORE]->(v:VioScoreTotal)
        OPTIONAL MATCH (v)-[:HAS_DIMENSION]->(d:Dimension)
        OPTIONAL MATCH (d)-[:HAS_CATEGORY]->(c:Category)
        OPTIONAL MATCH (c)-[:HAS_ATTRIBUTE]->(a:Attribute)
        RETURN r AS Region, v AS VioScoreTotal, d AS Dimension, c AS Category, a AS Attribute
    """

    tree_df = db_driver.execute_query_with_labels(query=query)
    if tree_df.empty:
        return None
    region_dictionary = {}
    category_dict = {}
    i = 1
    for region in tree_df["Region"].unique():
        region_label = list(region.labels)
        region_label.remove("Region")
        region_label.append("Region")
        region_dictionary = {
            "labels": region_label,
            "index": f'{i}',
            "code": region["region_code"],
            "name": region["region_name"],
            "children": []
        }
        region_df = tree_df[tree_df["Region"] == region]

        j = 1
        for vioscore_total in region_df["VioScoreTotal"].unique():
            vioscore_label = list(vioscore_total.labels)
            vioscore_label.remove("VioScoreTotal")
            vioscore_label.append("VioScoreTotal")
            vioscore_dict = {
                "labels": vioscore_label,
                "index": f'{i}.{j}',
                "code": vioscore_total['region_code'],
                "vioscore": vioscore_total['value'],
                "children": [

                ]
            }
            region_dictionary['children'].append(vioscore_dict)
            vioscore_df = region_df[region_df["VioScoreTotal"] == vioscore_total]

            k = 1
            for dimension in vioscore_df["Dimension"].unique():
                dimension_label = list(dimension.labels)
                dimension_label.remove("Dimension")
                dimension_label.append("Dimension")
                dimension_dict = {
                    "labels": dimension_label,
                    "index": f"{i}.{j}.{k}",
                    "code": dimension['region_code'],
                    "vioscore": dimension['value'],
                    "children": [

                    ]
                }
                vioscore_dict['children'].append(dimension_dict)
                dimension_df = vioscore_df[vioscore_df["Dimension"] == dimension]

                l = 1
                for category in dimension_df["Category"].unique():
                    if category != 'None':
                        category_label = list(category.labels)
                        category_label.remove("Category")
                        category_label.append("Category")
                        category_dict = {
                            "labels": category_label,
                            "index": f"{i}.{j}.{k}.{l}",
                            "code": category['region_code'],
                            "vioscore": category['value'],
                            "children": [

                            ]
                        }
                        dimension_dict['children'].append(category_dict)
                    category_df = dimension_df[dimension_df["Category"] == category]

                    m = 1
                    for attribute in category_df["Attribute"].unique():
                        if attribute != 'None':
                            attribute_label = list(attribute.labels)
                            attribute_label.remove("Attribute")
                            attribute_label.append("Attribute")
                            attribute_dict = {
                                "labels": attribute_label,
                                "index": f"{i}.{j}.{k}.{l}.{m}",
                                "code": attribute['region_code'],
                                "vioscore": attribute['value']
                            }
                            category_dict['children'].append(attribute_dict)
                        m += 1
                    l += 1
                k += 1
            j += 1
        i += 1
    return region_dictionary


def region_type_list(db_driver: Neo4jDriver, region_type: str):
    query = f"""
    MATCH (r: Region: {region_type})
    RETURN r
    """

    result = db_driver.execute_query(query=query)

    return result


def query_country_province(db_driver: Neo4jDriver, country_name: str):
    query = """
MATCH (c: Country {name: $country_name})-[]->(p: Province)
WITH p.code AS region_code, c, p
MATCH (r: Region: Province {region_code: region_code})
RETURN r """

    params = {
        'country_name': country_name
    }

    res = db_driver.execute_query(query=query, params=params)
    res = [dict(res["r"]) for res in res]

    return res


def query_province_municipality(db_driver: Neo4jDriver, province_name: str):
    query = """
MATCH (p: Province {name: $province_name})-[]->(m: Municipality)
WITH m.code AS region_code, p, m
MATCH (r: Region: Municipality {region_code: region_code})
RETURN r"""

    params = {
        'province_name': province_name
    }

    res = db_driver.execute_query(query=query, params=params)
    res = [dict(res["r"]) for res in res]

    return res


def query_municipality_district(db_driver: Neo4jDriver, municipality_name: str):
    query = """
MATCH (m: Municipality {name: $municipality_name})-[]->(d: District)
WITH d.code AS region_code, d, m
MATCH (r: Region: District {region_code: region_code})
RETURN r"""

    params = {
        'municipality_name': municipality_name
    }

    res = db_driver.execute_query(query=query, params=params)
    res = [dict(res["r"]) for res in res]

    return res


def query_district_neighbourhood(db_driver: Neo4jDriver, district_name: str):
    query = """
MATCH (d: District {name: $district_name})-[]->(n: Neighbourhood)
WITH n.code AS region_code, d, n
MATCH (r: Region: Neighbourhood {region_code: region_code})
RETURN r
"""

    params = {
        'district_name': district_name
    }

    res = db_driver.execute_query(query=query, params=params)

    res = [dict(res["r"]) for res in res]

    return res
