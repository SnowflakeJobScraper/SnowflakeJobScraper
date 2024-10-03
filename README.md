# Snowflake Job Scraper

## Project Description

This project is an automated system for scraping job postings from Snowflake's career page. 
It consists of a series of Python scripts that sequentially fetch, process, and analyze job posting data.

## Project Structure

The project consists of the following main scripts:

1. `00_search_jobs.py`: Fetches the list of job postings from Snowflake's career page.
2. `10_fetch_job_pages.py`: Downloads detailed pages for each job posting.
3. `20_extract_job_details_from_saved_job_pages.py`: Extracts job details from the downloaded pages.
4. `30_merge_job_details.py`: Merges job details into a single file.
5. `40_join_all.py`: Combines data from the job list and job details.
6. `50_archive.py`: Archives the output directory by renaming it with a timestamp.

Additionally, the project includes helper files:

- `config.py`: Contains project configuration.
- `fetch_page.py`: Implements a function for fetching web pages.
- `sanitize_filename.py`: Contains a function for cleaning file names.
- `find_and_run_scripts.py`: Searches for and runs scripts in the correct order.

## Requirements

- Python 3.x
- Libraries: requests, pandas

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/SnowflakeJobScraper/SnowflakeJobScraper.git
   ```
2. Navigate to the project directory:
   ```
   cd SnowflakeJobScraper
   ```
2. Navigate to the source directory:
   ```
   cd src
   ```
4. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the entire pipeline, execute:

```
python find_and_run_scripts.py
```

This will run all scripts in the appropriate order, including the archiving process at the end.

## Output

The scripts generate output files in the `output` directory:

- 00: HTML files with job listing pages, JSON files with job listing data
- 10: HTML files with job details
- 20: JSON and TXT files with job details

- and JSON and XLSX files with combined job posting data

After the scraping process is complete, the `50_archive.py` script renames the `output` directory to `output-YYYYMMDD-HHMMSS`, where `YYYYMMDD-HHMMSS` is the current timestamp. This allows for easy tracking of different scraping runs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
