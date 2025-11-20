# Lab Overview
this project is about how to handle 2 table from different file and how to merge
the two table with same same key and some are not.

## Project Structure
-README.md -> this file
-Cities.csv -> data file
-Countries.csv -> another data file
-procssing.py -> code file

## Design Overview
1.class DataLoader
class that handle loading csv file
-load_csv -> load csv file and return in list of dict

2.class DB
class that collect all table in list
-insert -> add table to list
-search -> medhod to find the table that user want and return that table

3.class Table
class that collect data from file that use DataLoader to convert
-convert -> method that try to convert text in float then return if can
-filter -> method that return thing that match the following condition
-aggreate -> method that use to calculated average, min or max
-merged -> method that use to mixed the two table into one

## Test and Run by
run and test with the given code