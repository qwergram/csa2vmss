namespace CloudServiceSeperator
{
    partial class PreCs2Vm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.CS2VMTabs = new System.Windows.Forms.TabControl();
            this.SelectProjectTab = new System.Windows.Forms.TabPage();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            this.SelectFolderButton = new System.Windows.Forms.Button();
            this.LocationHintLabel = new System.Windows.Forms.Label();
            this.CS2VMTabs.SuspendLayout();
            this.SelectProjectTab.SuspendLayout();
            this.SuspendLayout();
            // 
            // CS2VMTabs
            // 
            this.CS2VMTabs.Controls.Add(this.SelectProjectTab);
            this.CS2VMTabs.Controls.Add(this.tabPage2);
            this.CS2VMTabs.Location = new System.Drawing.Point(12, 12);
            this.CS2VMTabs.Name = "CS2VMTabs";
            this.CS2VMTabs.SelectedIndex = 0;
            this.CS2VMTabs.Size = new System.Drawing.Size(1037, 660);
            this.CS2VMTabs.TabIndex = 0;
            // 
            // SelectProjectTab
            // 
            this.SelectProjectTab.Controls.Add(this.LocationHintLabel);
            this.SelectProjectTab.Controls.Add(this.SelectFolderButton);
            this.SelectProjectTab.Location = new System.Drawing.Point(4, 29);
            this.SelectProjectTab.Name = "SelectProjectTab";
            this.SelectProjectTab.Padding = new System.Windows.Forms.Padding(3);
            this.SelectProjectTab.Size = new System.Drawing.Size(1029, 627);
            this.SelectProjectTab.TabIndex = 0;
            this.SelectProjectTab.Text = "Select Project Directory";
            this.SelectProjectTab.UseVisualStyleBackColor = true;
            // 
            // tabPage2
            // 
            this.tabPage2.Location = new System.Drawing.Point(4, 29);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage2.Size = new System.Drawing.Size(1029, 627);
            this.tabPage2.TabIndex = 1;
            this.tabPage2.Text = "tabPage2";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // SelectFolderButton
            // 
            this.SelectFolderButton.Location = new System.Drawing.Point(6, 6);
            this.SelectFolderButton.Name = "SelectFolderButton";
            this.SelectFolderButton.Size = new System.Drawing.Size(204, 40);
            this.SelectFolderButton.TabIndex = 1;
            this.SelectFolderButton.Text = "Select Project Directory";
            this.SelectFolderButton.UseVisualStyleBackColor = true;
            this.SelectFolderButton.Click += new System.EventHandler(this.SelectFolderButton_Click);
            // 
            // LocationHintLabel
            // 
            this.LocationHintLabel.AutoSize = true;
            this.LocationHintLabel.Location = new System.Drawing.Point(219, 16);
            this.LocationHintLabel.Name = "LocationHintLabel";
            this.LocationHintLabel.Size = new System.Drawing.Size(0, 20);
            this.LocationHintLabel.TabIndex = 2;
            // 
            // PreCs2Vm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1061, 684);
            this.Controls.Add(this.CS2VMTabs);
            this.Name = "PreCs2Vm";
            this.Text = "Pre-Script Cloud Service to VM";
            this.CS2VMTabs.ResumeLayout(false);
            this.SelectProjectTab.ResumeLayout(false);
            this.SelectProjectTab.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TabControl CS2VMTabs;
        private System.Windows.Forms.TabPage SelectProjectTab;
        private System.Windows.Forms.TabPage tabPage2;
        private System.Windows.Forms.Button SelectFolderButton;
        private System.Windows.Forms.Label LocationHintLabel;
    }
}

