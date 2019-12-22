FROM python:3.6

ARG project_dir=/app/

ADD requirements.txt $project_dir
ADD hojo_detection_system/app.py $project_dir
ADD hojo_detection_system/modules $project_dir/modules/
ADD hojo_detection_system/curation $project_dir/curation/
ADD hojo_detection_system/query $project_dir/query/
ADD hojo_detection_system/feature_vecs_csv/ $project_dir/feature_vecs_csv/

WORKDIR $project_dir

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]