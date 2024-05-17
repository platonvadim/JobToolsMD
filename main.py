from api.scraper.delucru_md import ParseDelucru


def main():
    # job_url = input("Enter delucru url: ")
    job_url = "https://www.delucru.md/job/64190"
    parser = ParseDelucru(job_url=job_url)
    print(parser)


if __name__ == '__main__':
    main()
