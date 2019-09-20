#!/usr/bin/env python
# encoding: utf-8
import logging
import optparse
import sys

# simple CLI for wistia.
import wistia.client

log = logging.getLogger("wistiapy")


def main(args=None):

    DESC = "Wistia python-based command line client."

    if len(sys.argv) < 2:
        sys.argv.append("-h")

    parser = optparse.OptionParser(usage="wistia.py [options]", description=DESC)

    parser.add_option("-c", "--cred", dest="cred", help="your API key", action="store")
    parser.add_option(
        "-p",
        "--projects",
        dest="list_projects",
        help="list all projects",
        action="store_true",
    )
    parser.add_option(
        "-m",
        "--medias",
        dest="list_medias",
        help="list all medias",
        action="store_true",
    )

    (options, args) = parser.parse_args()

    if not options.cred:
        raise Exception("Please supply your credentials with -c KEY")

    # list projects.
    w = wistia.client.WistiaClient("api", options.cred)
    if options.list_projects:
        projects = w.list_projects()
        for p in projects:
            print(f"{p.id}, {p.name}, {p.mediaCount}")

    # list all medias for a project.
    if options.list_medias:
        medias = w.list_medias()
        for m in medias:
            print(f"{m.id}, {m.name}, {m.duration}")

    # create an embed code for media.


if __name__ == "__main__":
    main()
