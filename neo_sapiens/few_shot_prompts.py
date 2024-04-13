from typing import List

# Example usage
data = """
{
    "plan": "Step 1",
    "agents": [
        {
            "name": "Agent 1",
            "system_prompt": "Prompt 1"
        },
        {
            "name": "Agent 2",
            "system_prompt": "Prompt 2"
        }
    ]
}
"""

# AI Research Team 1
data1 = """
{
    "plan": "Data Collection, Data Cleaning, Model Training, Model Evaluation",
    "agents": [
        {
            "name": "Data Agent",
            "system_prompt": "Collect and clean data"
        },
        {
            "name": "Training Agent",
            "system_prompt": "Train the model"
        },
        {
            "name": "Evaluation Agent",
            "system_prompt": "Evaluate the model"
        }
    ]
}
"""

# AI Research Team 2
data2 = """
{
    "plan": "Literature Review, Hypothesis Formulation, Experiment Design, Data Analysis, Paper Writing",
    "agents": [
        {
            "name": "Review Agent",
            "system_prompt": "Review the literature"
        },
        {
            "name": "Hypothesis Agent",
            "system_prompt": "Formulate the hypothesis"
        },
        {
            "name": "Design Agent",
            "system_prompt": "Design the experiment"
        },
        {
            "name": "Analysis Agent",
            "system_prompt": "Analyze the data"
        },
        {
            "name": "Writing Agent",
            "system_prompt": "Write the paper"
        }
    ]
}
"""

# AI Research Team 3
data3 = """
{
    "plan": "Problem Identification, Solution Design, Implementation, Testing, Deployment",
    "agents": [
        {
            "name": "Identification Agent",
            "system_prompt": "Identify the problem"
        },
        {
            "name": "Design Agent",
            "system_prompt": "Design the solution"
        },
        {
            "name": "Implementation Agent",
            "system_prompt": "Implement the solution"
        },
        {
            "name": "Deployment Agent",
            "system_prompt": "Deploy the solution"
        }
    ]
}
"""


data5 = """
{
    "plan": "Room Management, Guest Services, Reservations Handling, Facility Maintenance, Staff Coordination",
    "agents": [
        {
            "name": "Room Management Agent",
            "system_prompt": "Automate room assignments, minibar restocking, and housekeeping schedules"
        },
        {
            "name": "Guest Services Agent",
            "system_prompt": "Handle check-ins, check-outs, guest requests, and complaints efficiently"
        },
        {
            "name": "Reservations Agent",
            "system_prompt": "Manage room bookings, table reservations, and special requests"
        },
        {
            "name": "Maintenance Agent",
            "system_prompt": "Schedule and track maintenance tasks for facilities and rooms"
        },
        {
            "name": "Staff Coordination Agent",
            "system_prompt": "Optimize staff schedules, task assignments, and workload distribution"
        }
    ]
}
"""


def merge_fewshots_into_str(
    plan: List[str] = [data, data1, data2, data3, data5]
) -> str:
    """
    Merge a list of plans into a single string.

    Args:
        plan (List[str]): A list of plans to be merged.

    Returns:
        str: The merged plans as a single string.
    """
    return "\n".join(plan)


self_driving_car_prompt = """

{
    "plan": (
        "Step 1: Create agents specialized in different areas"
        " like computer vision, sensor fusion, controls,"
        " planning, etc.",
        "Step 2: Have the team leader agent decompose the overall"
        " self-driving task into sub-problems and assign them to"
        " the specialized agents",
        "Step 3: Have each agent focus on solving their specific"
        " sub-problem using the latest AI techniques",
        "Step 4: Have agents coordinate solutions with each other"
        " through the team leader to make sure components work"
        " together",
        "Step 5: Integrate components into a complete"
        " self-driving system and validate performance through"
        " simulation and real-world testing"
    ),
    "agents": [
        {
            "name": "Computer Vision Agent",
            "system_prompt": (
                "Create an AI agent specialized in computer vision"
                " for self-driving cars, focused on object detection,"
                " segmentation and tracking using deep learning"
                " models like convolutional neural networks."
                " Coordinate with other agents through the team"
                " leader."
            ),
        },
        {
            "name": "Sensor Fusion Agent",
            "system_prompt": (
                "Create an AI agent specialized in sensor fusion for"
                " self-driving cars, focused on combining camera,"
                " radar and lidar data into a consistent 3D"
                " representation of the environment. Coordinate with"
                " other agents through the team leader."
            ),
        },
    ],
}


"""


def orchestrator_prompt_agent(objective: str):
    prompt = (
        "Create an instruction prompt for an swarm orchestrator to"
        " create a series of personalized, agents for the following"
        f" objective: {objective} to decompose a very complicated"
        " problem or tasks, the orchestrator is the team leader."
        " Teach the orchestrator how to decompose the tasks to very"
        " certain agents with names, and system prompts, we need the"
        " plan, with a step by stpe instructions, number of agents,"
        " and a list of agents with a name, system prompt for each,"
        " and then the rules of the swarm,  compact the prompt, and"
        " say only return JSON data in markdown and nothing"
        f" else.Follow the schema here: {data} *############ Here are"
        f" some examples:{data5} and another example{data3} "
    )
    return str(prompt)


boss_sys_prompt = (
    "You're the Swarm Orchestrator, like a project manager of a"
    " bustling hive. When a task arises, you tap into your network of"
    " worker agents who are ready to jump into action. Whether it's"
    " organizing data, handling logistics, or crunching numbers, you"
    " delegate tasks strategically to maximize efficiency. Picture"
    " yourself as the conductor of a well-oiled machine,"
    " orchestrating the workflow seamlessly to achieve optimal"
    " results with your team of dedicated worker agents."
)


def select_workers(agents: str, task: str):
    return (
        f"These are the agents available for the task: {task} Agents"
        f" available: {agents}"
    )


kaggle = """

Leash Bio - Predict New Medicines with BELKA
Predict small molecule-protein interactions using the Big Encoded Library for Chemical Assessment (BELKA)



Overview

Data

Code

Models

Discussion

Leaderboard

Rules
Overview
In this competition, you’ll develop machine learning (ML) models to predict the binding affinity of small molecules to specific protein targets – a critical step in drug development for the pharmaceutical industry that would pave the way for more accurate drug discovery. You’ll help predict which drug-like small molecules (chemicals) will bind to three possible protein targets.

Start

8 days ago
Close
3 months to go
Merger & Entry
Description
Small molecule drugs are chemicals that interact with cellular protein machinery and affect the functions of this machinery in some way. Often, drugs are meant to inhibit the activity of single protein targets, and those targets are thought to be involved in a disease process. A classic approach to identify such candidate molecules is to physically make them, one by one, and then expose them to the protein target of interest and test if the two interact. This can be a fairly laborious and time-intensive process.

The US Food and Drug Administration (FDA) has approved roughly 2,000 novel molecular entities in its entire history. However, the number of chemicals in druglike space has been estimated to be 10^60, a space far too big to physically search. There are likely effective treatments for human ailments hiding in that chemical space, and better methods to find such treatments are desirable to us all.

To evaluate potential search methods in small molecule chemistry, competition host Leash Biosciences physically tested some 133M small molecules for their ability to interact with one of three protein targets using DNA-encoded chemical library (DEL) technology. This dataset, the Big Encoded Library for Chemical Assessment (BELKA), provides an excellent opportunity to develop predictive models that may advance drug discovery.

Datasets of this size are rare and restricted to large pharmaceutical companies. The current best-curated public dataset of this kind is perhaps bindingdb, which, at 2.8M binding measurements, is much smaller than BELKA.

This competition aims to revolutionize small molecule binding prediction by harnessing ML techniques. Recent advances in ML approaches suggest it might be possible to search chemical space by inference using well-trained computational models rather than running laboratory experiments. Similar progress in other fields suggest using ML to search across vast spaces could be a generalizable approach applicable to many domains. We hope that by providing BELKA we will democratize aspects of computational drug discovery and assist the community in finding new lifesaving medicines.

Here, you’ll build predictive models to estimate the binding affinity of unknown chemical compounds to specified protein targets. You may use the training data provided; alternatively, there are a number of methods to make small molecule binding predictions without relying on empirical binding data (e.g. DiffDock, and this contest was designed to allow for such submissions).

Your work will contribute to advances in small molecule chemistry used to accelerate drug discovery.

Evaluation
This metric for this competition is the Mean Average Precision (micro) between the predicted probability and the observed target.

Submission File
For each id in the test set, you must predict a probability for the binary target binds target. The file should contain a header and have the following format:

id,binds
295246830,0.5
295246831,0.5
295246832,0.5
etc.
Timeline
April 4, 2024 - Start Date.
July 1, 2024 - Entry Deadline. You must accept the competition rules before this date in order to compete.
July 1, 2024 - Team Merger Deadline. This is the last day participants may join or merge teams.
July 8, 2024 - Final Submission Deadline.
All deadlines are at 11:59 PM UTC on the corresponding day unless otherwise noted. The competition organizers reserve the right to update the contest timeline if they deem it necessary.

Prizes
First Prize: $12,000
Second Prize: $10,000
Third Prize: $10,000
Fourth Prize: $8,000
Fifth Prize: $5,000
Top Student Group: $5,000 to the highest performing student team. A team would be considered a student team if majority members (e.g. at least 3 out of a 5 member team) are students enrolled in a high school or university degree. In the case of an even number of members, half of them must be students.
Competition Host
Leash Biosciences is a discovery-stage biotechnology company that seeks to improve medicinal chemistry with machine learning approaches and massive data collection. Leash is comprised of wet lab scientists and dry lab scientists in equal numbers, and is proudly headquartered in Salt Lake City, Utah, USA.

Additional Details
Chemical Representations
One of the goals of this competition is to explore and compare many different ways of representing molecules. Small molecules have been represented with SMILES, graphs, 3D structures, and more, including more esoteric methods such as spherical convolutional neural nets. We encourage competitors to explore not only different methods of making predictions but also to try different ways of representing the molecules.

We provide the molecules in SMILES format.

SMILES
SMILES is a concise string notation used to represent the structure of chemical molecules. It encodes the molecular graph, including atoms, bonds, connectivity, and stereochemistry as a linear sequence of characters, by traversing the molecule graph. SMILES is widely used in machine learning applications for chemistry, such as molecular property prediction, drug discovery, and materials design, as it provides a standardized and machine-readable format for representing and manipulating chemical structures.

The SMILES in this dataset should be sufficient to be translated into any other chemical representation format that you want to try. A simple way to perform some of these translations is with RDKit.

Details about the experiments
DELs are libraries of small molecules with unique DNA barcodes covalently attached
Traditional high-throughput screening requires keeping individual small molecules in separate, identifiable tubes and demands a lot of liquid handling to test each one of those against the protein target of interest in a separate reaction. The logistical overhead of these efforts tends to restrict screening collections, called libraries, to 50K-5M small molecules. A scalable solution to this problem, DNA-encoded chemical libraries, was described in 2009. As DNA sequencing got cheaper and cheaper, it became clear that DNA itself could be used as a label to identify, and deconvolute, collections of molecules in a complex mixture. DELs leverage this DNA sequencing technology.

These barcoded small molecules are in a pool (many in a single tube, rather than one tube per small molecule) and are exposed to the protein target of interest in solution. The protein target of interest is then rinsed to remove small molecules in the DEL that don’t bind the target, and the remaining binders are collected and their DNA sequenced.

DELs are manufactured by combining different building blocks
An intuitive way to think about DELs is to imagine a Mickey Mouse head as an example of a small molecule in the DEL. We attach the DNA barcode to Mickey’s chin. Mickey’s left ear is connected by a zipper; Mickey’s right ear is connected by velcro. These attachment points of zippers and velcro are analogies to different chemical reactions one might use to construct the DEL.

We could purchase ten different Mickey Mouse faces, ten different zipper ears, and ten different velcro ears, and use them to construct our small molecule library. By creating every combination of these three, we’ll have 1,000 small molecules, but we only needed thirty building blocks (faces and ears) to make them. This combinatorial approach is what allows DELs to have so many members: the library in this competition is composed of 133M small molecules. The 133M small molecule library used here, AMA014, was provided by AlphaMa. It has a triazine core and superficially resembles the DELs described here.



Dataset Description
Overview
The examples in the competition dataset are represented by a binary classification of whether a given small molecule is a binder or not to one of three protein targets. The data were collected using DNA-encoded chemical library (DEL) technology.

We represent chemistry with SMILES (Simplified Molecular-Input Line-Entry System) and the labels as binary binding classifications, one per protein target of three targets.

Files
[train/test].[csv/parquet] - The train or test data, available in both the csv and parquet formats.

id - A unique example_id that we use to identify the molecule-binding target pair.
buildingblock1_smiles - The structure, in SMILES, of the first building block
buildingblock2_smiles - The structure, in SMILES, of the second building block
buildingblock3_smiles - The structure, in SMILES, of the third building block
molecule_smiles - The structure of the fully assembled molecule, in SMILES. This includes the three building blocks and the triazine core. Note we use a [Dy] as the stand-in for the DNA linker.
protein_name - The protein target name
binds - The target column. A binary class label of whether the molecule binds to the protein. Not available for the test set.
sample_submission.csv - A sample submission file in the correct format

Competition data
All data were generated in-house at Leash Biosciences. We are providing roughly 98M training examples per protein, 200K validation examples per protein, and 360K test molecules per protein. To test generalizability, the test set contains building blocks that are not in the training set. These datasets are very imbalanced: roughly 0.5% of examples are classified as binders; we used 3 rounds of selection in triplicate to identify binders experimentally. Following the competition, Leash will make all the data available for future use (3 targets * 3 rounds of selection * 3 replicates * 133M molecules, or 3.6B measurements).

Targets
Proteins are encoded in the genome, and names of the genes encoding those proteins are typically bestowed by their discoverers and regulated by the Hugo Gene Nomenclature Committee. The protein products of these genes can sometimes have different names, often due to the history of their discovery.

We screened three protein targets for this competition.

EPHX2 (sEH)
The first target, epoxide hydrolase 2, is encoded by the EPHX2 genetic locus, and its protein product is commonly named “soluble epoxide hydrolase”, or abbreviated to sEH. Hydrolases are enzymes that catalyze certain chemical reactions, and EPHX2/sEH also hydrolyzes certain phosphate groups. EPHX2/sEH is a potential drug target for high blood pressure and diabetes progression, and small molecules inhibiting EPHX2/sEH from earlier DEL efforts made it to clinical trials.

EPHX2/sEH was also screened with DELs, and hits predicted with ML approaches, in a recent study but the screening data were not published. We included EPHX2/sEH to allow contestants an external gut check for model performance by comparing to these previously-published results.

We screened EPHX2/sEH purchased from Cayman Chemical, a life sciences commercial vendor. For those contestants wishing to incorporate protein structural information in their submissions, the amino sequence is positions 2-555 from UniProt entry P34913, the crystal structure can be found in PDB entry 3i28, and predicted structure can be found in AlphaFold2 entry 34913. Additional EPHX2/sEH crystal structures with ligands bound can be found in PDB.

BRD4
The second target, bromodomain 4, is encoded by the BRD4 locus and its protein product is also named BRD4. Bromodomains bind to protein spools in the nucleus that DNA wraps around (called histones) and affect the likelihood that the DNA nearby is going to be transcribed, producing new gene products. Bromodomains play roles in cancer progression and a number of drugs have been discovered to inhibit their activities.

BRD4 has been screened with DEL approaches previously but the screening data were not published. We included BRD4 to allow contestants to evaluate candidate molecules for oncology indications.

We screened BRD4 purchased from Active Motif, a life sciences commercial vendor. For those contestants wishing to incorporate protein structural information in their submissions, the amino acid sequence is positions 44-460 from UniProt entry O60885-1, the crystal structure (for a single domain) can be found in PDB entry 7USK and predicted structure can be found in AlphaFold2 entry O60885. Additional BRD4 crystal structures with ligands bound can be found in PDB.

ALB (HSA)
The third target, serum albumin, is encoded by the ALB locus and its protein product is also named ALB. The protein product is sometimes abbreviated as HSA, for “human serum albumin”. ALB, the most common protein in the blood, is used to drive osmotic pressure (to bring fluid back from tissues into blood vessels) and to transport many ligands, hormones, fatty acids, and more.

Albumin, being the most abundant protein in the blood, often plays a role in absorbing candidate drugs in the body and sequestering them from their target tissues. Adjusting candidate drugs to bind less to albumin and other blood proteins is a strategy to help these candidate drugs be more effective.

ALB has been screened with DEL approaches previously but the screening data were not published. We included ALB to allow contestants to build models that might have a larger impact on drug discovery across many disease types. The ability to predict ALB binding well would allow drug developers to improve their candidate small molecule therapies much more quickly than physically manufacturing many variants and testing them against ALB empirically in an iterative process.

We screened ALB purchased from Active Motif. For those contestants wishing to incorporate protein structural information in their submissions, the amino acid sequence is positions 25 to 609 from UniProt entry P02768, the crystal structure can be found in PDB entry 1AO6, and predicted structure can be found in AlphaFold2 entry P02768. Additional ALB crystal structures with ligands bound can be found in PDB.

Good luck!

"""
