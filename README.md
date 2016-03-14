# Pumpjack

Pumpjack is a tool for documenting APIs that are implemented in
multiple languages.

For now, I'm using it to document just one API, the
[Qpid Proton](http://qpid.apache.org/proton/index.html) event-driven
messaging API.

See the
[current published results](http://home.apache.org/~jross/pumpjack/).

## Project layout

    Makefile              # Defines the make targets
    python/               # Python library code
    scripts/              # Scripts called by Makefile rules
    api/                  # API definition files
    input/                # Markdown and HTML input files
    output/               # HTML output

## Make targets

    make render           # Generate content under output/
    make clean            # Removes output/
    make publish          # Publish the output to home.apache.org
    make help             # Print help for make targets
