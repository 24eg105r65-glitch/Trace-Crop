$ErrorActionPreference = 'Stop'

$source = Resolve-Path 'TraceCrop_Project_Report.docx'
$outDir = Join-Path (Get-Location) 'report_more_tmp'
if (Test-Path $outDir) { Remove-Item -LiteralPath $outDir -Recurse -Force }
New-Item -ItemType Directory -Path $outDir | Out-Null

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($source, (Resolve-Path $outDir))

function Escape-Xml([string]$s) {
    if ($null -eq $s) { return '' }
    return [System.Security.SecurityElement]::Escape($s)
}

function RunXml([string]$text, [bool]$bold = $false, [string]$size = '24') {
    $b = if ($bold) { '<w:b/>' } else { '' }
    return "<w:r><w:rPr>$b<w:sz w:val=""$size""/><w:szCs w:val=""$size""/></w:rPr><w:t xml:space=""preserve"">$(Escape-Xml $text)</w:t></w:r>"
}

function ParaXml([string]$text, [string]$align = 'both', [bool]$bold = $false, [string]$size = '24') {
    return "<w:p><w:pPr><w:jc w:val=""$align""/><w:spacing w:after=""160"" w:line=""276"" w:lineRule=""auto""/></w:pPr>$(RunXml $text $bold $size)</w:p>"
}

function HeadingXml([string]$text, [int]$level = 1) {
    $size = if ($level -eq 1) { '32' } elseif ($level -eq 2) { '28' } else { '24' }
    return "<w:p><w:pPr><w:pStyle w:val=""Heading$level""/><w:spacing w:before=""300"" w:after=""180""/><w:jc w:val=""left""/></w:pPr>$(RunXml $text $true $size)</w:p>"
}

function BulletXml([string]$text) {
    return "<w:p><w:pPr><w:ind w:left=""720"" w:hanging=""360""/><w:spacing w:after=""80""/></w:pPr>$(RunXml '- ' $false '24')$(RunXml $text $false '24')</w:p>"
}

function TableXml([object[]]$rows) {
    $xml = '<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders><w:top w:val="single" w:sz="6" w:space="0" w:color="808080"/><w:left w:val="single" w:sz="6" w:space="0" w:color="808080"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="808080"/><w:right w:val="single" w:sz="6" w:space="0" w:color="808080"/><w:insideH w:val="single" w:sz="6" w:space="0" w:color="808080"/><w:insideV w:val="single" w:sz="6" w:space="0" w:color="808080"/></w:tblBorders></w:tblPr>'
    foreach ($row in $rows) {
        $xml += '<w:tr>'
        foreach ($cell in $row) {
            $xml += '<w:tc><w:tcPr><w:tcW w:w="4500" w:type="dxa"/></w:tcPr>' + (ParaXml ([string]$cell) 'left' $false '22') + '</w:tc>'
        }
        $xml += '</w:tr>'
    }
    return $xml + '</w:tbl>'
}

function AddSection([string]$heading, [string[]]$paras, [string[]]$bullets = @(), [object[]]$table = @()) {
    $xml = HeadingXml $heading 1
    foreach ($p in $paras) { $xml += ParaXml $p }
    foreach ($b in $bullets) { $xml += BulletXml $b }
    if ($table.Count -gt 0) { $xml += TableXml $table }
    return $xml
}

$append = ''

$append += AddSection '25. DETAILED METHODOLOGY' @(
    'The methodology followed for TraceCrop was incremental and iterative. The project was not built in a single step; instead, each role and workflow was developed, tested, and improved gradually. First, the Firebase configuration and authentication workflow were prepared. Then signup, login, and role-based navigation were implemented. After authentication became stable, individual dashboards were developed for farmer, distributor, quality auditor, government, and consumer users.',
    'The next phase focused on data modeling. The users collection stores account role and public ID. The crops collection stores crop batch details, farmer identity, distributor identity, audit status, logistics status, and consumer-facing traceability data. Once the data model became stable, Firestore security rules were adjusted to allow only valid role-specific updates.',
    'The final phase focused on user experience and deployment. Long Firebase UIDs were replaced with public IDs. Browser alerts were replaced with animated notifications. The translator was moved away from the top navigation. The app was then deployed using Firebase Hosting and Firestore rules deployment.'
) @(
    'Requirement study and workflow identification.',
    'Firebase setup and authentication configuration.',
    'Role-based dashboard design.',
    'Firestore data model and rules implementation.',
    'UI refinement and notification improvements.',
    'Testing, validation, and Firebase deployment.'
)

$append += AddSection '26. FEASIBILITY STUDY' @(
    'Technical feasibility is high because the system uses standard browser technologies and Firebase services. The frontend can run on any modern browser, while Firebase provides managed authentication, database, and hosting services. This reduces backend complexity and makes the project suitable for academic implementation.',
    'Operational feasibility is also strong because the system is divided by user role. A farmer does not need to understand government monitoring features, and a consumer does not need to access internal dashboards. Each role sees a focused interface that matches its responsibility.',
    'Economic feasibility is favorable for prototype development. Firebase free-tier resources, static hosting, and open web technologies reduce cost. The system can be demonstrated without maintaining a dedicated server.'
) @(
    'Technical feasibility: Achieved using Firebase, HTML, CSS, and JavaScript.',
    'Operational feasibility: Achieved through role-specific dashboards.',
    'Economic feasibility: Achieved through free-tier cloud tools.',
    'Schedule feasibility: Achieved by developing one workflow at a time.'
)

$append += AddSection '27. SECURITY DESIGN' @(
    'TraceCrop uses Firebase Authentication to identify users and Firestore security rules to restrict database operations. Authentication alone is not sufficient because a logged-in user should not be allowed to update any record. Therefore, the rules check ownership, assigned distributor identity, and user role before allowing updates.',
    'Farmers can create crops and update their own crop records, but they cannot modify auditor-only fields. Quality auditors can update fields such as quality grade, audit notes, audit timestamp, and report URL. Distributors can update shipment-related fields after they are assigned to a crop. Public consumers can read crop records for traceability but cannot write to the database.',
    'This separation of responsibilities protects important crop data while still allowing public traceability. In a production version, additional server-side validation and audit logs can be introduced for stronger protection.'
) @(
    'Authentication protects access to dashboards.',
    'Firestore rules protect crop ownership and update scope.',
    'Public IDs improve usability without replacing internal secure UIDs.',
    'Consumers can read trace data but cannot modify records.',
    'Auditors and distributors can update only their relevant fields.'
)

$append += AddSection '28. DATA FLOW AND WORKFLOW' @(
    'The farmer workflow begins with account creation. After login, the farmer registers a crop by entering crop name, variety, sowing date, location, fertilizer details, and optional image. The system generates a public batch code and stores the crop as Unassigned.',
    'After the crop is registered, the farmer can transfer it to a distributor by entering the distributor public ID. The system searches the users collection, verifies that the target account role is Distributor, and stores the distributor internal UID and public ID in the crop document.',
    'The quality auditor workflow begins by opening the audit dashboard. The auditor searches by batch ID or crop name, updates grade, enters notes, and submits report information. The consumer workflow begins by entering a batch code on the trace page, after which the crop journey is displayed.'
) @(
    'Farmer registration flow: Form input -> batch code -> crop document.',
    'Transfer flow: Distributor public ID -> validation -> crop assignment.',
    'Audit flow: Search crop -> grade and notes -> Firestore update.',
    'Distributor flow: Accept transfer -> update status and location.',
    'Consumer flow: Batch search -> product timeline display.'
)

$append += AddSection '29. DETAILED TESTING' @(
    'Testing was performed at multiple levels. Syntax testing was performed by parsing inline JavaScript from all HTML files. Page availability testing was performed using HTTP checks on the local static server. Firebase deployment also validated Firestore rules compilation and hosting upload.',
    'Functional testing focused on role-based workflows. Signup and login were tested for multiple roles. Farmer crop registration was tested with and without image upload. Transfer was tested with missing distributor ID, invalid public ID, non-distributor public ID, and valid distributor public ID. Auditor search was tested with batch code, crop name, and crop variety.',
    'User-interface testing focused on whether important controls were visible and not disturbing the layout. The translator widget was moved to the bottom-left, alerts were converted to animated notifications, and transfer was moved out of registration.'
) $null @(
    @('Feature', 'Validation Performed'),
    @('Signup/Login', 'Role profile creation and redirect checked'),
    @('Farmer Registration', 'Crop created with batch code and Unassigned distributor'),
    @('Transfer', 'Distributor public ID validation checked'),
    @('Auditor Search', 'Batch ID, crop name, and variety search checked'),
    @('Notifications', 'Alerts displayed as animated toast messages'),
    @('Deployment', 'Firebase Hosting and Firestore rules deployed successfully')
)

$append += AddSection '30. DEPLOYMENT DETAILS' @(
    'The application was deployed to Firebase Hosting under the project tracecrop-a756a. Hosting deployment uploaded static assets from the public folder. Firestore rules and indexes were also deployed so that the live application uses the latest database security configuration.',
    'The deployment command used was firebase deploy --only "hosting,firestore" --project tracecrop-a756a. The deployment completed successfully and released the live hosting version.',
    'The live project URL is https://tracecrop-a756a.web.app. This confirms that the project is not only locally functional but also hosted online for demonstration.'
) @(
    'Hosting provider: Firebase Hosting.',
    'Project ID: tracecrop-a756a.',
    'Live URL: https://tracecrop-a756a.web.app.',
    'Deployed resources: Hosting, Firestore rules, Firestore indexes.'
)

$append += AddSection '31. RISK ANALYSIS' @(
    'Every software project has risks. In TraceCrop, the main risks are related to data accuracy, role misuse, internet dependency, and prototype-level upload handling. Since the system depends on users entering correct data, data validation is important. Since Firebase is cloud-based, internet connectivity is also required.',
    'Security risks are reduced using Firestore rules, but a production system should add stronger admin review, audit logs, and backend validation. Image upload configuration should also be moved to a secure server-side flow in a future version.'
) @(
    'Risk: Incorrect data entry by users. Mitigation: Form validation and guided UI.',
    'Risk: Unauthorized updates. Mitigation: Firestore security rules.',
    'Risk: Internet dependency. Mitigation: Future PWA/offline support.',
    'Risk: Prototype image upload configuration. Mitigation: Future backend upload service.',
    'Risk: Public read access for traceability. Mitigation: Store only consumer-safe crop fields publicly.'
)

$append += AddSection '32. PROJECT TIMELINE' @(
    'The project can be divided into phases. Each phase builds on the previous one and adds a complete part of the traceability workflow.'
) $null @(
    @('Phase', 'Work Completed'),
    @('Phase 1', 'Requirement analysis and project setup'),
    @('Phase 2', 'Firebase configuration, signup, login, and role profiles'),
    @('Phase 3', 'Farmer crop registration and crop list'),
    @('Phase 4', 'Quality auditor dashboard and search'),
    @('Phase 5', 'Distributor transfer and shipment workflow'),
    @('Phase 6', 'Government dashboard and consumer trace page'),
    @('Phase 7', 'UI improvements, notifications, translator placement'),
    @('Phase 8', 'Testing, report preparation, and Firebase deployment')
)

$append += AddSection '33. LEARNING OUTCOMES' @(
    'The project provided practical experience in full-stack web application development using a serverless backend. It improved understanding of authentication, cloud database operations, role-based access, real-time listeners, deployment, and user interface design.',
    'The project also gave insight into how technical identifiers must be converted into user-friendly identifiers for real-world usability. The workflow changes, such as moving transfer after registration, showed the importance of matching software design with natural user behavior.'
) @(
    'Hands-on experience with Firebase Authentication and Firestore.',
    'Understanding of Firestore security rules and role-based access.',
    'Experience building responsive dashboards with Tailwind CSS.',
    'Experience deploying a web app to Firebase Hosting.',
    'Improved understanding of user-centered workflow design.'
)

$docPath = Join-Path $outDir 'word\document.xml'
$doc = Get-Content -Raw -LiteralPath $docPath
$doc = $doc -replace '<w:sectPr>', ($append + '<w:sectPr>')
Set-Content -LiteralPath $docPath -Value $doc -Encoding UTF8

$more = Join-Path (Get-Location) 'TraceCrop_Project_Report_More_Detailed.docx'
if (Test-Path $more) { Remove-Item -LiteralPath $more -Force }
[System.IO.Compression.ZipFile]::CreateFromDirectory((Resolve-Path $outDir), $more)
Copy-Item -LiteralPath $more -Destination $source -Force
Remove-Item -LiteralPath $outDir -Recurse -Force

Get-Item $source, $more | Select-Object Name, Length, LastWriteTime
