package net.legacyfabric.multifilament.task;

import java.io.IOException;

import org.gradle.api.file.DirectoryProperty;
import org.gradle.api.provider.Property;
import org.gradle.api.tasks.Input;
import org.gradle.api.tasks.OutputDirectory;
import org.gradle.api.tasks.TaskAction;

import net.fabricmc.mappingio.MappingWriter;
import net.fabricmc.mappingio.format.MappingFormat;

public abstract class MappingOutputTask extends MultiFilamentTask {
	public MappingOutputTask() {
	}

	@Input
	public abstract Property<MappingFormat> getOutputFormat();

	@OutputDirectory
	public abstract DirectoryProperty getOutputDir();

	void pre() throws IOException {
	}

	@TaskAction
	public final void run() throws IOException {
		this.pre();
		MappingWriter mappingWriter = MappingWriter.create(this.getOutputDir().getAsFile().get().toPath(), this.getOutputFormat().get());

		try {
			this.run(mappingWriter);
		} catch (Throwable var5) {
			if (mappingWriter != null) {
				try {
					mappingWriter.close();
				} catch (Throwable var4) {
					var5.addSuppressed(var4);
				}
			}

			throw var5;
		}

		if (mappingWriter != null) {
			mappingWriter.close();
		}
	}

	abstract void run(MappingWriter var1) throws IOException;
}
