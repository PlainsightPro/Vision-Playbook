# Autoscale Billing for Spark in Microsoft Fabric

> [!info] Purpose
> Autoscale Billing for Spark enables serverless, pay-as-you-go compute for Spark workloads in Microsoft Fabric. Once enabled, Spark jobs no longer consume the shared capacity, giving you the flexibility to scale Spark workloads independently and optimize costs.

## Requirements

| Requirement | Details |
|---|---|
| **Capacity** | Only available for Fabric F-SKUs (F2 and above). Not supported on P-SKUs or Fabric Trial capacities. |
| **Access** | You must be a Fabric Capacity Administrator to configure Autoscale Billing. |

> [!warning] Important
> Enabling, disabling, or reducing the Maximum Capacity Units will cancel all active Spark jobs running under Autoscale Billing to avoid billing overlaps.

## How to Configure Autoscale Billing for Spark

Follow these steps to enable and manage Autoscale Billing settings for a Fabric capacity:

1. **Navigate to the Microsoft Fabric Admin Portal**
   - Under the Governance and insights section, select Admin portal

2. **Access Capacity Settings**
   - From the left-hand menu, choose Capacity settings and go to the Fabric capacity tab
   - Select the capacity you want to configure

3. **Enable Autoscale Billing**
   - In the Capacity Settings page, scroll to the **Autoscale Billing for Fabric Spark** section
   - Enable the Autoscale Billing toggle

4. **Set Maximum Capacity Units (CU)**
   - Use the slider to set the Maximum Capacity Units (CU) you want to allocate to Spark jobs
   - The maximum limit available is based on:
     - The quota approved for your Azure subscription
     - The type of subscription you're using
   - You are only billed for the compute used, up to this limit
   - To increase quota, see [[#Request additional quotas|Request additional quotas]] below

5. **Save Your Settings**
   - Click Save to apply your configuration
   - Your Spark Pools can now utilize the new CU quota set by Autoscale Billing

> [!tip]
> Once Autoscale Billing is enabled, consider whether you can resize your shared Fabric capacity down (see [[#Optional: Resize and reset capacity for cost optimization|Optional: Resize and reset capacity]] below), since Spark workloads are now billed separately.

## Optional: Resize and Reset Capacity for Cost Optimization

After enabling Autoscale Billing, you can downsize your shared Fabric capacity if Spark workloads are no longer using it. This reduces the cost of your base capacity:

1. **Go to the Azure Portal**
   - Search for and select your Fabric capacity

2. **Reset Capacity Usage**
   - Click **Pause** to temporarily stop the capacity
   - This clears any active or unsmoothed Spark usage on the shared capacity
   - Wait 5 minutes, then click **Resume** to restart the capacity

3. **Resize to a Lower SKU**
   - Resize the capacity to a lower SKU that fits your remaining workloads (e.g., Power BI, Data Warehouse, Real-Time Intelligence, Databases)

> [!warning] Note
> Only Azure administrators can resize SKUs. This change is made in the Azure portal, not within Fabric settings.

## Monitor Billing and Usage

After enabling Autoscale Billing, use Azure's built-in cost management tools to track compute usage:

1. **Navigate to Azure Cost Analysis**
   - Go to the Azure portal
   - Select the Subscription linked to your Fabric capacity
   - In the subscription page, go to **Cost Analysis**

2. **Filter for Spark Usage**
   - Filter by the resource (Fabric capacity)
   - Look for the meter: **Autoscale for Spark Capacity Usage CU**
   - View real-time compute spend for Spark workloads using Autoscale Billing

## Request Additional Quotas

If your data engineering or data science workloads require a higher quota than your current maximum Capacity Unit (CU) limit, you can request an increase:

1. **Navigate to Azure Quotas**
   - Go to the Azure portal and sign in
   - In the search bar, type and select **Azure Quotas**

2. **Request a Quota Increase**
   - Choose **Microsoft Fabric** from the list of available services
   - Select the subscription associated with your Fabric capacity
   - Edit the quota limit by entering the new CU limit you need
   - Submit your quota request

3. **Wait for Approval**
   - Once approved, the new CU limits will be refreshed and applied to your Fabric capacity
   - This ensures your Autoscale Billing model can accommodate increased demand without interrupting Spark workloads

## Related Pages
- [[6. Capacity Management|Capacity Management]] — Overall capacity planning and monitoring
- [[4. Data Pipeline Patterns|Data Pipeline Patterns]] — Design Spark jobs for efficiency
- [[3. Lakehouse Architecture|Lakehouse Architecture]] — Understand medallion architecture patterns