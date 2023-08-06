{{ "{{/*" }} 
Expand the name of the chart.
{{ "*/}}" }} 
{{ "{{-" }} define "new_one.name" {{ "-}}" }}
{{ "{{-" }} default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" {{ "}}" }}
{{ "{{-" }} end {{ "}}" }}

{{ "{{/*" }} 
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
{{ "*/}}" }} 
{{ "{{-" }} define "new_one.fullname" {{ "-}}" }}
{{ "{{-" }} if .Values.fullnameOverride {{ "}}" }}
{{ "{{-" }} .Values.fullnameOverride | trunc 63 | trimSuffix "-" {{ "}}" }}
{{ "{{-" }} else {{ "}}" }}
{{ "{{-" }} $name := default .Chart.Name .Values.nameOverride {{ "}}" }}
{{ "{{-" }} if contains $name .Release.Name {{ "}}" }}
{{ "{{-" }} .Release.Name | trunc 63 | trimSuffix "-" {{ "}}" }}
{{ "{{-" }} else {{ "}}" }}
{{ "{{-" }} printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" {{ "}}" }}
{{ "{{-" }} end {{ "}}" }}
{{ "{{-" }} end {{ "}}" }}
{{ "{{-" }} end {{ "}}" }}

{{ "{{/*" }} 
Create chart name and version as used by the chart label.
{{ "*/}}" }} 
{{ "{{-" }} define "new_one.chart" {{ "-}}" }}
{{ "{{-" }} printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" {{ "}}" }}
{{ "{{-" }} end {{ "}}" }}

{{ "{{/*" }} 
Common labels
{{ "*/}}" }} 
{{ "{{-" }} define "new_one.labels" {{ "-}}" }}
helm.sh/chart: {{ "{{" }}  include "new_one.chart" . {{ "}}" }}
{{ "{{" }} include "new_one.selectorLabels" . {{ "}}" }}
{{ "{{-" }} if .Chart.AppVersion {{ "}}" }}
app.kubernetes.io/version: {{ "{{" }} .Chart.AppVersion | quote {{ "}}" }}
{{ "{{-" }} end {{ "}}" }}
app.kubernetes.io/managed-by: {{ "{{" }} .Release.Service {{ "}}" }}
{{ "{{-" }} end {{ "}}" }}

{{ "{{/*" }} 
Selector labels
{{ "*/}}" }} 
{{ "{{-" }} define "new_one.selectorLabels" {{ "-}}" }}
app.kubernetes.io/name: {{ "{{" }} include "new_one.name" . {{ "}}" }}
app.kubernetes.io/instance: {{ "{{" }} .Release.Name {{ "}}" }}
{{ "{{-" }} end {{ "}}" }}

{{ "{{/*" }} 
Create the name of the service account to use
{{ "*/}}" }} 
{{ "{{-" }} define "new_one.serviceAccountName" {{ "-}}" }}
{{ "{{-" }} if .Values.serviceAccount.create {{ "}}" }}
{{ "{{-" }} default (include "new_one.fullname" .) .Values.serviceAccount.name {{ "}}" }}
{{ "{{-" }} else {{ "}}" }}
{{ "{{-" }} default "default" .Values.serviceAccount.name {{ "}}" }}
{{ "{{-" }} end {{ "}}" }}
{{ "{{-" }} end {{ "}}" }}
