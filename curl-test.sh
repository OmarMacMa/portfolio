#!/bin/bash


POSTED=$(curl -s -X POST http://localhost:5000/api/time_line_post -d 'name=Jorge&email=jorge@gmail.com&content=Testing endpints with bash script')
echo "POST Response: "
echo $POSTED


GOT=$(curl -s http://localhost:5000/api/time_line_post)
echo "GET Response: "
echo $GOT

POSTID=$(echo $POSTED | jq '.id')
FILTER=".time_line_posts[] | select(.id == $POSTID)"
FOUND=$(echo "$GOT" | jq "$FILTER")

if [ -n "$FOUND" ]; then
	TLPID=$(echo $FOUND | jq '.id')
	echo "Timeline post found, id: $TLPID"
	DELETED=$(curl -s -X DELETE http://localhost:5000/api/time_line_post -d "id=$TLPID")
	if [ $? -eq 0 ]; then
		echo "Deleted, all tests passed"
	else
		echo "something went wrong deleting the timeline post"
	fi
else
	echo "Something went wrong"
fi

