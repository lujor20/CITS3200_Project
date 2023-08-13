# CITS3200_Project
This is the GIT repository for all code and similar resources.

<h1>Cheating Detection Tool</h1>

<h2>Description From Client</h2>
 <h3>Tool 1: </h3>
 document analysis tool When a student submits an assignment in the form of a Microsoft Word Document that was actually written by someone else various aspects of the document's metadata potentially provide clues that may help substantiate an allegation of cheating. It is often the case that when students obtain an essay or similar written by another person they lightly edit the document, for example, adding their name and institution. At times, it is possible that document Properties are wiped or provide insufficient data to conclude how the work was written. However, forensic techniques exist that can dig deeper into documents when they are unzipped as XML files. See: this https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7324152.

There are various clues in that can be drawn from the XML file that indicate potential cheating as outlines here https://doi.org/10.1007/s10805-019-09358-w and here https://doi.org/10.1007/978-3-031-12680-2_12

What I am proposing as a tool for the students to develop is a program (site etc) into which an MS Word document can be dropped or uploaded. The tool would then do the work of converting the file to a zip format, unzipping the file to its XML constituent parts, and analysing the relevant constituent parts to provide evidence to assess in cases of suspected cheating such as counts of revision identifiers, ratio of edited to words, versions of Word used, languages used in the document

In short, the tool would unzip and automate the analysis of cheating-relevant information in word documents. A really sophisticated version would also conduct a web search for any identified author or website author to see whether these are known cheating providers.

<h3>Tool 2</h3> 
This idea is simpler than the first. When students take online tests in LMS (Blackboard)it is possible to download a log the test activity that includes IP addresses from where the test was accessed, date and time, etc. This log is downloadable as a comma delimited file (*.csv), that people typically open in Excel.

When students outsource test completion to third parties well-known large-scale cheating providers are often off-shore in Kenya, China, Ukraine, and India or Pakistan. The second tool I propose would automatically search the IP column in the online test log and flag (highlight) suspicious activities such as logins from Kenya, logins from multiple IP addresses for the same student on repeatable tests, logins from discrepant locations at times that would make travel between the locations impossible, logins at unusual times (e.g. 12am-5am). Incorporating IP lookups into this process should be able to show whether addresses are VPNs or not.

An excellent tool would rank suspicious activity by counting and indicating when multiple red flags are apparent on the same test-taking incident (e.g., IP login from in Perth at 12am, followed by IP in Kenya, test taken at 3am). 

<li>Client: Guy Curtis</li>
<li>Phone: 0864883356</li>
<li>Email: guy.curtis@uwa.edu.au</li>
<li>Preferred contact: Email</li>
<li>Location: UWA</li>

# To Run The Program

### 1. Clone Remote Repository

```
git clone https://github.com/lujor20/CITS3200_Project.git
```

### 2. Create a virtual environment

```
python3 -m venv dev-env
```

### 3. Open the virtual environment
#### Using Windows Powershell

```
dev-env\Scripts\Activate.ps1
```

#### Using Windows Command Prompt

```
dev-env\bin\activate.bat
```

#### Using Linux/MacOS

```
source dev-env/bin/activate
```
### 4. Install the Required libraries

```
pip install -r requirements.txt
```

### 5. Run the tool

```
python3 rsid.py <docx file path>
```
#### Example:

```
python3 rsid.py test.docx
```

# Tool 1 Findings
## Forensics for Revision Identifiers 
Revision Identifiers (RSID) is a 32-bit value represented by eight hex numbers which are stored in OOXML document (e.g. Microsoft Word - docx).
RSID contains useful information such as traces left from the modification of the document which could serve as evidence to assess in cases of suspected cheating.
Here are some properties of RSID values:
<li>Probability of RSID value overlapping with pre-existing value is extremely low</li>
<li>RSID values differ between different editing session (period of editing which takes place between any two subsequent save actions)</li>
<li>RSID values are stored in "document.xml" and "settings.xml" files in the MS Word structure</li>
<li>Even after modifying or deleting the content, if at least one letter in the document remains for which RSID has already been assigned, the existing RSID remains in the document</li>
<li>Even if all the RSIDs in the "document.xml" file are deleted, the ones stored in the "settings.xml" file remain intact</li>
<li>If there is an MS Word file suspected of being a copy or a leaked file, all existing RSIDs are recorded within the "settings.xml" file, even if the user modifies or deletes the document content</li>
<li>RSID is not always copied and saved, but only under certain conditions. For RSID to be copied, the copied word or sentence must contain at least one customized font and not the default font (Calibri with font size 11)</li>
<li>If all the content the user wants to copy is in the default font, and it is copied and pasted into a new document or an existing document, the RSID assigned to the original file is not copied to the destination file</li>
<li>When the user copies the content from the original file into another file, the RSID is copied and stored in the "document.xml" file of the destination, but not in the "settings xml" file. Thus, if the RSID exists in the "document.xml" file but not in the "settings.xml" file, the user can see that this part is copied from the original file</li>




<h2>Analyzing Relevant XML Constituent Parts</h2>
<li>Metadata information are usually stored in the folder docProps</li>
<li>Two or more XML files are stored inside that folder:</li>
<li>        app.xml - stores metadata information extracted from the Word application itself</li>
<li>        core.xml - stores metadata from the document itself, such as the author name, last time it was printed, etc</li>
<li>The file _rels/.rels contains information about the structure of the document. It contains paths to the metadata information as well as the main XML document that contains the content of the document itself</li>
<li>An XML file called document.xml is the main document, containing most of the content of the document itself</li>


<h2>Suspicious Indicators</h2>
<li>Word has a total time edited file property. If the total editing time improbably large, maybe the file has been handed down over a number of years</li>
<li>AppVersion and OSVersion are data points that can be helpful in identifying discrepancies in a Word document. For example, if the OSVersion points to Windows 10, but none of the timestamps in the document are after 2013, you might want to take a closer look at that document</li>
<li>if someone has a Word document that is a few years old, or they are representing it as being a few years old, but it’s using a more recent, unique font, it is suspicious</li>
<li>It is alarming if you’ve got a five-page document that has an edit time of two minutes, or just one revision</li>
<li>By comparing the similarities between the document's temporary TMP file and autosaved ASD files can help in finding out if there are copy pasted content in the document</li>

<h2>Tools to explore</h2>
<li>X-Ways v19.5 and FTK v6.4</li>
<li>Olefile and ExifTool</li>
<li>OfficeDissector</li>
<li>https://github.com/abctemp90/Grouping_document_tool</li>
