#!/bin/sh

echo "Initiating job"
python -m main
status=$?

if [ "$status" -ne 0 ]; then
  echo "Job failed with exit code $status. Terminating container."
else
  echo "Job finished successfully. Terminating container."
fi

exit $status
