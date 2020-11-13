# -*- coding: utf-8 -*-

import clr
import sys

clr.AddReference("Interop.SolidEdge")
clr.AddReference("System")
clr.AddReference("System.Runtime.InteropServices")

import System.Collections
import System.Runtime.InteropServices as SRI
import System

from SolidEdgeAssembly.QueryPropertyConstants import seQueryPropertyCategory
from SolidEdgeAssembly.QueryPropertyConstants import seQueryPropertyCustom
from SolidEdgeAssembly.QueryPropertyConstants import seQueryPropertyReference
from SolidEdgeAssembly.QueryConditionConstants import seQueryConditionContains
from SolidEdgeAssembly.QueryConditionConstants import seQueryConditionIsNot
from SolidEdgeAssembly.QueryConditionConstants import seQueryConditionIs

from query import CriteriaProperties
from helper import create_query
from System import Console


# import SolidEdgeAssembly as SEAssembly

__project__ = "query_references"
__author__ = "recs"
__version__ = "0.0.3"
__update__ = "2020-11-13"


def create_various_queries(asm, search_subassemblies):
    print("part: %s\n" % asm.Name)
    assert asm.Type == 3, "This macro only works on .asm document."

    #  REFERENCE QUERIES
    # ==================

    # "Reference [Excluded from Assembly Reports]"
    ref_reports = CriteriaProperties(
        seQueryPropertyReference,
        "Reference",
        seQueryConditionIs,
        "Excluded from Assembly Reports",
    )
    create_query(
        asm.Queries,
        "Reference [Excluded from Assembly Reports]",
        [ref_reports.criterias],
        search_subassemblies
    )

    # "Reference [Not displayed in drawing views]"
    not_display_drawings = CriteriaProperties(
        seQueryPropertyReference,
        "Reference",
        seQueryConditionIs,
        "Not displayed in drawing views",
    )
    create_query(
        asm.Queries,
        "Reference [Not displayed in drawing views]",
        [not_display_drawings.criterias],
        search_subassemblies
    )

    # "Reference [Displayed as Reference in Drawing Views]"
    ref_drawings = CriteriaProperties(
        seQueryPropertyReference,
        "Reference",
        seQueryConditionIs,
        "Displayed as Reference in Drawing Views",
    )
    create_query(
        asm.Queries,
        "Reference [Displayed as Reference in Drawing Views]",
        [ref_drawings.criterias],
        search_subassemblies
    )


def stop():
    sys.exit()


def remove_all_queries(assembly):
    print("queries number: %s" % assembly.Queries.Count)
    # Remove query in the collection of queries
    created_queries = [
        "Reference [Displayed as Reference in Drawing Views]",
        "Reference [Excluded from Assembly Reports]",
        "Reference [Not displayed in drawing views]",
    ]

    for query in created_queries:
        assembly.Queries.Remove(query)
        print("[DELETED] %s " % query)


def would_do_like_to_create_or_remove_all_queries():
    response = raw_input(
    """
    Press [*] to create queries with all parts even those in the subassemblies.
    Press [-] to create queries without the parts in the subassemblies.
    Press [/] to delete all queries.
    """
    ).lower()
    choice = {"*": "create_various_queries_all", "-": "create_various_queries_edited_level", "/": "remove_all_queries"}
    return choice.get(response)


def user_confirmation_to_continue():
    response = raw_input(
        """Would you like to create reference queries in the Select Tools? (Press y/[Y] to proceed.)"""
    )
    if response.lower() in ["y", "yes"]:
        pass
    else:
        print("Process canceled")
        sys.exit()


def main():
    try:
        user_confirmation_to_continue()
        answer = would_do_like_to_create_or_remove_all_queries()
        application = SRI.Marshal.GetActiveObject("SolidEdge.Application")
        assembly = application.ActiveDocument

        if answer == "create_various_queries_all":
            create_various_queries(assembly, True)

        elif answer == "create_various_queries_edited_level":
            create_various_queries(assembly, False)

        elif answer == "remove_all_queries":
            remove_all_queries(assembly)

        else:
            pass

    except Exception as ex:
        print(ex)

    finally:
        raw_input("\nPress any key to exit...")
        stop()


if __name__ == "__main__":
    print(
        "%s\n--author:%s --version:%s --last-update :%s\n"
        % (__project__, __author__, __version__, __update__)
    )
    main()
